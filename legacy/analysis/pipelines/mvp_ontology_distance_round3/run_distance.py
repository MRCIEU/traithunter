import json
import math
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Union

import numpy as np
import ray
import requests
import simple_parsing
from loguru import logger
from pydash import py_
from simple_parsing import field
from typing_extensions import TypedDict

from analysis_funcs import paths, settings

import pandas as pd  # noqa
import janitor  # noqa

import local_utils  # isort:skip


NUM_WORKERS = 4
TRIAL_SAMPLE = 30
data_dir = paths.data_root
SUB_PROJ_NAME = "mvp-ontology-terms-2023-03"
OUTPUT_DIR = data_dir / "output" / SUB_PROJ_NAME


@dataclass
class Conf:
    dry_run: bool = field(alias="dry-run", action="store_true")
    trial: bool = field(action="store_true")
    num_workers: int = NUM_WORKERS
    echo_step: int = 200
    es_url: str = settings.es_url
    trial_sample: int = TRIAL_SAMPLE
    trial_suffix: str = ""
    top_match_fraction: float = 0.03
    input_clean_df_path: Union[str, Path] = OUTPUT_DIR / "clean_terms.csv"
    input_failed_df_path: Union[str, Path] = OUTPUT_DIR / "encode_fails.csv"
    output_distance_dir_path: Optional[Union[str, Path]] = None


@dataclass
class SourceInfo(TypedDict):
    source: str
    count: int


@dataclass
class Sample(TypedDict):
    id: str
    term: str
    term_clean: str
    source: str


@dataclass
class QueryRes(TypedDict):
    ent_id: str
    ent_term: str
    cosine_similarity: float


@dataclass
class QueryResPerSource(TypedDict):
    source: str
    candidates: List[QueryRes]


@dataclass
class QueryResTotal(TypedDict):
    id: str
    term: str
    source: str
    results: Optional[List[QueryResPerSource]]


def make_conf() -> Conf:

    conf: Conf = simple_parsing.parse(Conf)
    conf.trial_suffix = "" if not conf.trial else "_trial"
    conf.input_clean_df_path = Path(conf.input_clean_df_path)
    conf.output_distance_dir_path = Path(OUTPUT_DIR / f"distance{conf.trial_suffix}")
    if conf.output_distance_dir_path.exists():
        shutil.rmtree(str(conf.output_distance_dir_path))
    conf.output_distance_dir_path.mkdir(exist_ok=True)
    logger.info(f"conf {conf}")
    return conf


@ray.remote(num_cpus=1)
class Worker:
    def __init__(
        self,
        idx: int,
        conf: Conf,
        source_info_list: List[SourceInfo],
        failed_id_list: List[str],
    ):
        self.idx = idx
        self.conf = conf
        self.es_url = self.conf.es_url
        self.source_info_list = source_info_list
        self.failed_id_list = failed_id_list

    def process_chunk(self, sample_list: List[Sample]) -> List[QueryResTotal]:
        res: List[QueryResTotal] = [
            {
                "id": _["id"],
                "term": _["term"],
                "source": _["source"],
                "results": self.query_by_source(
                    target_id=_["id"],
                    target_source=_["source"],
                    idx=idx,
                    total=len(sample_list),
                ),
            }
            for idx, _ in enumerate(sample_list)
        ]
        return res

    def query_by_source(
        self, target_id: str, target_source: str, idx: int, total: int
    ) -> Optional[List[QueryResPerSource]]:
        if idx % self.conf.echo_step == 0:
            logger.info(f"worker #{self.idx}: {idx}/{total}")
        if target_id in self.failed_id_list:
            logger.info(f"{target_id} in failed_id_list, ignore the rest")
            return None
        target_vector = self.get_target_vector(target_id, target_source)
        if len(target_vector) == 0:
            logger.info(f"{target_id} empty vector, ignore the rest")
            return None
        res: List[QueryResPerSource] = [
            {
                "source": _["source"],
                "candidates": self.query(
                    target_id=target_id,
                    target_vector=target_vector,
                    source=_["source"],
                    source_count=_["count"],
                ),
            }
            for _ in self.source_info_list
        ]
        return res

    def get_target_vector(self, target_id: str, target_source: str) -> List[float]:
        index_name = local_utils.get_es_index_for_source(
            source=target_source, trial=self.conf.trial
        )
        url = self.conf.es_url + f"/{index_name}/_search"
        payload = {
            "query": {
                "term": {"ent_id": target_id},
            },
            "_source": ["ent_id", "vector_term", "vector"],
        }
        r = requests.get(url, json=payload)
        try:
            r.raise_for_status()
            results = r.json()["hits"]["hits"]
            res = results[0]["_source"]["vector"]
        except Exception as e:
            logger.info(
                f"ES problem, vector phase, target_id: {target_id}, target_source: {target_source}, {e}"
            )
            res = []
        return res

    def query(
        self, target_id: str, target_vector: List[float], source: str, source_count: int
    ) -> List[QueryRes]:
        index_name = local_utils.get_es_index_for_source(
            source=source, trial=self.conf.trial
        )
        num_cands = int(np.round(self.conf.top_match_fraction * source_count))
        url = self.conf.es_url + f"/{index_name}/_knn_search"
        payload = {
            "knn": {
                "field": "vector",
                "query_vector": target_vector,
                "k": num_cands,
                "num_candidates": num_cands * 1.2,
            },
            "_source": ["ent_id", "ent_term"],
        }
        r = requests.get(url, json=payload)
        try:
            r.raise_for_status()
            results = r.json()["hits"]["hits"]
        except Exception as e:
            logger.info(f"ES problem, query phase, target_id: {target_id}, {e}")
            results = []
        res: List[QueryRes] = [
            {
                "ent_id": _["_source"]["ent_id"],
                "ent_term": _["_source"]["ent_term"],
                "cosine_similarity": _["_score"],
            }
            for _ in results
        ]
        return res


def main_process(
    sample: List[Sample], workers: List[Worker], conf: Conf
) -> List[QueryResTotal]:
    chunks = py_.chunk(sample, size=math.ceil(len(sample) / conf.num_workers))
    chunk_res: List[List[QueryResTotal]] = ray.get(
        [
            worker.process_chunk.remote(sample_list=chunks[idx])  # type: ignore
            for idx, worker in enumerate(workers)
        ]
    )
    res: List[QueryResTotal] = py_.flatten(chunk_res)
    return res


def main():
    # conf
    conf = make_conf()

    # init
    r = requests.get(conf.es_url)
    assert r.ok
    clean_df = pd.read_csv(conf.input_clean_df_path)
    failed_df = pd.read_csv(conf.input_failed_df_path)
    failed_id_list = failed_df["id"].tolist()
    source_list = clean_df["source"].drop_duplicates().tolist()
    source_count = (
        clean_df["source"]
        .value_counts()
        .to_frame()
        .reset_index(drop=False)
        .to_dict(orient="records")
    )
    source_info_list: List[SourceInfo] = [
        {
            "source": _["index"],
            "count": _["source"],
        }
        for _ in source_count
    ]

    sample_all = (
        clean_df
        if not conf.trial
        else clean_df.groupby("source").head(conf.trial_sample)
    )
    sample_all.info()

    if not conf.dry_run:
        if ray.is_initialized():
            ray.shutdown()
        ray.init(num_cpus=conf.num_workers)
        print(ray.available_resources())

        logger.info("processing init")
        workers = [
            Worker.remote(idx, conf=conf, source_info_list=source_info_list, failed_id_list=failed_id_list)  # type: ignore
            for idx, _ in enumerate(range(conf.num_workers))
        ]
        for idx, source in enumerate(source_list):
            sample_df = sample_all[sample_all["source"] == source]
            sample: List[Sample] = sample_df[
                ["id", "term", "term_clean", "source"]
            ].to_dict(orient="records")
            chunk_size = 4000
            if len(sample) > chunk_size:
                sample_chunks = py_.chunk(sample, size=chunk_size)
            else:
                sample_chunks = [sample]
            logger.info(f"{source} split into {len(sample_chunks)} chunks")
            for idxx, sample in enumerate(sample_chunks):
                logger.info(
                    f"#{idx}/{len(source_list)} start processing source {source}, chunk #{idxx}"
                )
                distance_res: pd.DataFrame = main_process(
                    sample=sample, workers=workers, conf=conf
                )
                output_path = (
                    conf.output_distance_dir_path / f"{source}_chunk{idxx}.json"
                )
                with output_path.open("w") as f:
                    json.dump(distance_res, f)
        logger.info("processing done")

        if ray.is_initialized():
            ray.shutdown()


if __name__ == "__main__":
    main()
