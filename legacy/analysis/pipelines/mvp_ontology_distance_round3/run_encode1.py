import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import ray
import simple_parsing
import spacy
from loguru import logger
from pydash import py_
from simple_parsing import field
from typing_extensions import TypedDict

from analysis_funcs import paths

import pandas as pd  # noqa
import janitor  # noqa


NUM_WORKERS = 2
TRIAL_SAMPLE = 500
data_dir = paths.data_root
SUB_PROJ_NAME = "mvp-ontology-terms-2023-06"
INPUT_DIR = data_dir / "source" / SUB_PROJ_NAME
OUTPUT_DIR = data_dir / "output" / SUB_PROJ_NAME
INPUT_FILE = INPUT_DIR / "new_phenotypes_for_encoding_31MAY.csv"
MODEL_PATH = paths.models["scispacy_lg"]


@dataclass
class Conf:
    dry_run: bool = field(alias="dry-run", action="store_true")
    trial: bool = field(action="store_true")
    input_file: Union[str, Path] = field(alias="input-file", default=INPUT_FILE)
    output_dir: Union[str, Path] = field(alias="output-dir", default=OUTPUT_DIR)
    model_path: Union[str, Path] = field(alias="model-path", default=MODEL_PATH)
    num_workers: int = NUM_WORKERS
    echo_step: int = 200
    trial_sample: int = TRIAL_SAMPLE
    trial_suffix: str = ""
    clean_df_path: Union[str, Path] = OUTPUT_DIR / "clean_terms.csv"
    output_encode_fails_path: Optional[Union[str, Path]] = None
    output_encode_res_path: Optional[Union[str, Path]] = None


class EncodeInputItem(TypedDict):
    id: str
    term: str
    term_clean: str


class EncodeRes(TypedDict):
    id: str
    term: str
    term_clean: str
    term_vector: List[float]


def make_conf() -> Conf:
    conf: Conf = simple_parsing.parse(Conf)
    conf.trial_suffix = "" if not conf.trial else "_trial"
    conf.input_file = Path(conf.input_file)
    conf.output_dir = Path(conf.output_dir)
    conf.model_path = Path(conf.model_path)
    conf.clean_df_path = Path(conf.clean_df_path)
    conf.output_encode_fails_path = (
        conf.output_dir / f"encode_fails{conf.trial_suffix}.csv"
    )
    conf.output_encode_res_path = conf.output_dir / f"encodings{conf.trial_suffix}.json"
    logger.info(f"conf {conf}")
    return conf


def clean_input(source_df: pd.DataFrame) -> pd.DataFrame:
    def _clean_term(text: str) -> str:
        text = text.replace("obsolete", " ")
        # scispacy model does not properly tokenize slashes without spaces
        # so enforce
        # for slashes already with spaces this does not affect much
        text = text.replace("/", " / ").strip()
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
    sample: List[EncodeInputItem], encoders: List[ItemEncoder], conf: Conf
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


def main_process(
    encoders: List[ItemEncoder],
    sample_df: pd.DataFrame,
    conf: Conf,
) -> Tuple[List[EncodeRes], pd.DataFrame]:
    # sample
    sample: List[EncodeInputItem] = sample_df.to_dict(orient="records")
    logger.info(f"main process: start processing {len(sample)} items")
    # encode items
    encode_res = main_encode(sample=sample, encoders=encoders, conf=conf)
    logger.info(f"len(encode_res) {len(encode_res)}")
    # encode diagnostics
    encode_res_fail = get_encode_fails(encode_res=encode_res)
    failed_list = encode_res_fail["id"].tolist() if len(encode_res_fail) > 0 else []
    # bulk index
    encode_res_slim: List[EncodeRes] = [
        _ for _ in encode_res if _["id"] not in failed_list
    ]
    # done
    logger.info("main process: done")
    res = encode_res_slim, encode_res_fail
    return res


def main():
    # conf
    conf = make_conf()

    # init
    # ## read
    source_df = pd.read_csv(conf.input_file).rename(
        columns={
            "unique_ID": "id",
            "description": "term",
        }
    )
    # ## sample to process
    clean_df = clean_input(source_df)
    clean_df.to_csv(conf.clean_df_path, index=False)
    sample_df = clean_df if not conf.trial else clean_df.head(conf.trial_sample)
    sample_df.info()

    # main main
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

        encode_res, encode_res_fails = main_process(
            encoders=encoders, sample_df=sample_df, conf=conf
        )
        encode_res_fails.to_csv(conf.output_encode_fails_path, index=False)
        with conf.output_encode_res_path.open("w") as f:
            json.dump(encode_res, f)

        if ray.is_initialized():
            ray.shutdown()


if __name__ == "__main__":
    main()
