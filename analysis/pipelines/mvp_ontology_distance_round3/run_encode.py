import argparse
import math
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import ray
import requests
import spacy
from loguru import logger
from pydash import py_
from simple_parsing import ArgumentParser
from typing_extensions import TypedDict

from analysis_funcs import es, paths, settings

import pandas as pd  # noqa
import janitor  # noqa

from local_utils import es_config  # isort:skip


class EncodeInputItem(TypedDict):
    id: str
    term: str
    term_clean: str


class EncodeRes(TypedDict):
    id: str
    term: str
    term_clean: str
    term_vector: List[float]


class IndexRecord(TypedDict):
    ent_id: str
    ent_term: str
    vector_term: str
    vector: List[float]


def get_es_index_for_source(source: str, trial: bool) -> str:
    trial_str = "--trial" if trial else ""
    res = "mvp-ontology-source-{source}{trial_str}".format(
        source=source.lower(), trial_str=trial_str
    )
    return res


def make_conf() -> argparse.Namespace:
    NUM_WORKERS = 4
    TRIAL_SAMPLE = 500
    data_dir = paths.data_root
    SUB_PROJ_NAME = "mvp-ontology-terms-2023-03"
    INPUT_DIR = data_dir / "source" / SUB_PROJ_NAME
    OUTPUT_DIR = data_dir / "output" / SUB_PROJ_NAME
    INPUT_FILE = (
        INPUT_DIR / "ontology_source_descriptors_for_distance_calc_16MAR2023.csv"
    )
    MODEL_PATH = paths.models["scispacy_lg"]

    parser = ArgumentParser()
    parser.add_argument("--input-file", type=str, help="input file", default=INPUT_FILE)
    parser.add_argument(
        "--output-dir", type=str, help="output directory", default=OUTPUT_DIR
    )
    parser.add_argument("--trial", help="trial", action="store_true")
    parser.add_argument("--dry-run", help="dry run", action="store_true")

    conf = parser.parse_args()
    assert conf.input_file.exists(), conf.input_file
    conf.output_dir = Path(conf.output_dir)
    conf.output_dir.mkdir(exist_ok=True)
    conf.model_path = MODEL_PATH
    assert conf.model_path.exists(), conf.model_path
    conf.num_workers = NUM_WORKERS
    conf.es_url = settings.es_url
    conf.trial_sample = TRIAL_SAMPLE
    conf.trial_suffix = "" if not conf.trial else "_trial"
    conf.clean_df_path = conf.output_dir / "clean_terms.csv"
    conf.output_encode_fails_path = (
        conf.output_dir / f"encode_fails{conf.trial_suffix}.csv"
    )
    logger.info(f"conf {conf}")
    return conf


def clean_input(source_df: pd.DataFrame) -> pd.DataFrame:
    def _clean_term(text: str) -> str:
        text = text.replace("obsolete_", "")
        # scispacy model does not properly tokenize slashes without spaces
        # so enforce
        # for slashes already with spaces this does not affect much
        text = text.replace("/", " / ")
        return text

    clean_df = source_df.assign(term_clean=lambda df: df["term"].apply(_clean_term))
    return clean_df


@ray.remote(num_cpus=1)
class ItemEncoder:
    def __init__(self, idx: int, model_path: Path):
        self.idx = f"Encoder {idx}"
        logger.info(f"{self.idx}: Init model")
        self.nlp = spacy.load(model_path)
        logger.info(f"{self.idx}: Model loaded")

    def encode_items(self, idx: int, total: int, item: EncodeInputItem) -> EncodeRes:
        echo_step = 200
        if idx % echo_step == 0:
            logger.info(f"{self.idx}: # {idx} / {total}")
        term = item["term_clean"]
        vector = self.nlp(term).vector.tolist()
        res: EncodeRes = {
            "id": item["id"],
            "term": term,
            "term_clean": term,
            "term_vector": vector,
        }
        return res

    def encode_chunk(self, item_list: List[Dict]) -> List[EncodeRes]:
        logger.info(f"{self.idx}: Start to process {len(item_list)} items")
        res = [
            self.encode_items(idx=idx, total=len(item_list), item=_)
            for idx, _ in enumerate(item_list)
        ]
        logger.info(f"{self.idx}: Finish process")
        return res


def get_encode_fails(encode_res: List[EncodeRes]) -> pd.DataFrame:
    def _check_fail(vector: List[float]) -> bool:
        # check if all elems in the vector are zero, and if so
        # it means the term fails to produce a corresponding vector
        res = not np.any(vector)
        return res

    encode_fails = pd.DataFrame(
        [
            {"id": _["id"], "term": _["term"], "term_clean": _["term_clean"]}
            for _ in encode_res
            if _check_fail(_["term_vector"])
        ]
    )
    return encode_fails


def main_encode(
    sample: List[EncodeInputItem], encoders: List[ItemEncoder], conf: argparse.Namespace
) -> List[EncodeRes]:
    chunks = py_.chunk(sample, size=math.ceil(len(sample) / conf.num_workers))
    chunk_res = ray.get(
        [
            encoder.encode_chunk.remote(chunks[idx])  # type: ignore
            for idx, encoder in enumerate(encoders)
        ]
    )
    res = py_.flatten(chunk_res)
    return res


def main_index(
    index_sample: List[IndexRecord], source: str, conf: argparse.Namespace
) -> None:
    index_name = get_es_index_for_source(source=source, trial=conf.trial)
    logger.info(
        f"ES: index {index_name}, start; indexing {len(index_sample):_} records"
    )
    if es.index_exists(conf.es_url, index_name):
        logger.info(f"ES: index {index_name}, exists, will overwrite")
        es.drop_index(conf.es_url, index_name)
    else:
        logger.info(f"ES: index {index_name}, not exist, will spawn")
    index_conf = es_config.make_es_index_conf()
    es.init_index(es_url=conf.es_url, index_name=index_name, config=index_conf)
    docs: List[Dict[str, Any]] = [_ for _ in index_sample]
    es.bulk_index(es_url=conf.es_url, index_name=index_name, docs=docs, logger_step=200)
    logger.info(f"ES: index {index_name}, done")


def main_process(
    source: str,
    encoders: List[ItemEncoder],
    sample_df: pd.DataFrame,
    conf: argparse.Namespace,
) -> pd.DataFrame:
    # sample
    sample: List[EncodeInputItem] = sample_df[sample_df["source"] == source].to_dict(
        orient="records"
    )
    logger.info(f"source {source}: start processing {len(sample)} items")
    # encode items
    encode_res = main_encode(sample=sample, encoders=encoders, conf=conf)
    logger.info(f"len(encode_res) {len(encode_res)}")
    # encode diagnostics
    encode_res_fail = get_encode_fails(encode_res=encode_res)
    failed_list = encode_res_fail["id"].tolist() if len(encode_res_fail) > 0 else []
    # bulk index
    index_sample: List[IndexRecord] = [
        {
            "ent_id": _["id"],
            "ent_term": _["term"],
            "vector_term": _["term"],
            "vector": _["term_vector"],
        }
        for _ in encode_res
        if _["id"] not in failed_list
    ]
    main_index(index_sample=index_sample, source=source, conf=conf)
    # done
    logger.info(f"source {source}: done")
    res = encode_res_fail
    return res


def main():
    # conf
    conf = make_conf()

    # init
    r = requests.get(conf.es_url)
    assert r.ok
    # ## read
    source_df = pd.read_csv(conf.input_file).rename(
        columns={
            "unique_ID": "id",
            "source_descriptions_clean": "term",
            "Source": "source",
        }
    )
    # ## sources
    source_list = source_df["source"].drop_duplicates().tolist()
    logger.info(f"source_list {source_list}")
    # ## sample to process
    clean_df = clean_input(source_df)
    clean_df.to_csv(conf.clean_df_path, index=False)
    sample_df = (
        clean_df
        if not conf.trial
        else clean_df.groupby("source").head(conf.trial_sample)
    )
    sample_df.info()

    # iterate over each source to process
    if not conf.dry_run:
        if ray.is_initialized():
            ray.shutdown()
        ray.init(num_cpus=conf.num_workers)
        print(ray.available_resources())

        logger.info("encoder init")
        encoders = [
            ItemEncoder.remote(idx=idx, model_path=conf.model_path)  # type: ignore
            for idx, _ in enumerate(range(conf.num_workers))
        ]
        logger.info("encoder spawned")

        encode_res_fails_all = []
        for _ in source_list:
            encode_res_fail = main_process(
                source=_, encoders=encoders, sample_df=sample_df, conf=conf
            )
            encode_res_fails_all.append(encode_res_fail)
        encode_res_fails_all = pd.concat(encode_res_fails_all)
        encode_res_fails_all.to_csv(conf.output_encode_fails_path, index=False)

        if ray.is_initialized():
            ray.shutdown()


if __name__ == "__main__":
    main()
