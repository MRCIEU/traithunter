import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import ray
import spacy
from pydash import py_
from simple_parsing import ArgumentParser

from analysis_funcs import now, paths

import pandas as pd  # noqa
import janitor  # noqa

from local_utils import data_types  # isort:skip


def make_conf() -> argparse.Namespace:
    NUM_WORKERS = 4
    TRIAL_SAMPLE = 500
    data_dir = paths.data_root
    SUB_PROJ_NAME = "mvp-ontology-terms-2023-01"
    OUTPUT_DIR = data_dir / "output" / SUB_PROJ_NAME
    INPUT_FILE = OUTPUT_DIR / "efo_terms.csv"
    MODEL_PATH = paths.models["scispacy_lg"]

    parser = ArgumentParser()
    parser.add_argument("--input-file", type=str, help="input file", default=INPUT_FILE)
    parser.add_argument(
        "--output-dir", type=str, help="output directory", default=OUTPUT_DIR
    )
    parser.add_argument("--trial", help="trial", action="store_true")
    parser.add_argument("--dry-run", help="dry run", action="store_true")

    conf = parser.parse_args()
    conf.output_dir = Path(conf.output_dir)
    assert conf.output_dir.exists(), conf.output_dir
    conf.model_path = MODEL_PATH
    assert conf.model_path.exists(), conf.model_path
    conf.num_workers = NUM_WORKERS
    conf.trial_sample = TRIAL_SAMPLE
    conf.trial_suffix = "" if not conf.trial else "_trial"
    conf.output_encode_path = conf.output_dir / f"encode{conf.trial_suffix}.json"
    conf.output_encode_fails_path = (
        conf.output_dir / f"encode_fails{conf.trial_suffix}.csv"
    )
    print(conf)
    return conf


@ray.remote(num_cpus=1)
class ItemEncoder:
    def __init__(self, idx: int, model_path: Path):
        self.idx = f"Encoder {idx}"
        print(f"{now()} {self.idx}: Init model")
        self.nlp = spacy.load(model_path)
        print(f"{now()} {self.idx}: Model loaded")

    def encode_items(self, idx: int, total: int, item: Dict[str, Any]):
        echo_step = 200
        if idx % echo_step == 0:
            print(f"{now()} {self.idx}: # {idx} / {total}")
        term_col = "efo_term_clean"
        term = item[term_col]
        vector = self.nlp(term).vector.tolist()
        res = {
            "efo_id": item["efo_id"],
            "term": term,
            "term_vector": vector,
        }
        return res

    def encode_chunk(self, item_list: List[Dict]):
        print(f"{now()} {self.idx}: Start to process {len(item_list)} items")
        res = [
            self.encode_items(idx=idx, total=len(item_list), item=_)
            for idx, _ in enumerate(item_list)
        ]
        print(f"{now()} {self.idx}: Finish process")
        return res


def encode_main(
    chunks: List[List[Dict[str, Any]]], conf: argparse.Namespace
) -> List[Dict[str, Any]]:

    encoders = [
        ItemEncoder.remote(idx=idx, model_path=conf.model_path)  # type: ignore
        for idx, _ in enumerate(range(conf.num_workers))
    ]

    chunk_res = ray.get(
        [
            encoder.encode_chunk.remote(chunks[idx])
            for idx, encoder in enumerate(encoders)
        ]
    )
    res = py_.flatten(chunk_res)
    return res


def check_encode_fails(encode_res: List[Dict[str, Any]]) -> pd.DataFrame:
    def _check_fail(vector: List[float]) -> bool:
        # check if all elems in the vector are zero, and if so
        # it means the term fails to produce a corresponding vector
        res = not np.any(vector)
        return res

    encode_fails = pd.DataFrame(
        [
            {
                "efo_id": _["efo_id"],
                "term": _["term"],
                "fail": _check_fail(_["term_vector"]),
            }
            for _ in encode_res
        ]
    )
    encode_fails = (
        encode_fails[encode_fails["fail"]].drop(columns=["fail"]).reset_index(drop=True)
    )
    return encode_fails


def main():
    # # init
    conf = make_conf()

    if ray.is_initialized():
        ray.shutdown()
    ray.init(num_cpus=conf.num_workers)
    print(ray.available_resources())

    # # term chunks
    efo_terms = (
        pd.read_csv(conf.input_file)
        .also(lambda df: data_types.CleanedDf.validate(df))
        .also(lambda df: print("efo terms: ", df.info()))
        .to_dict(orient="records")
    )
    if conf.trial:
        efo_terms = efo_terms[: conf.trial_sample]
    chunks = py_.chunk(efo_terms, size=math.ceil(len(efo_terms) / conf.num_workers))
    print(f"{now()} len chunks {len(chunks)}")
    print(f"{now()} len chunks[0] {len(chunks[0])}")

    # # encode
    print(f"{now()} # Encode")

    if not conf.dry_run:
        encode_res = encode_main(chunks=chunks, conf=conf)
        print(f"{now()} len encode_res {len(encode_res)}")
        with conf.output_encode_path.open("w") as f:
            json.dump(encode_res, f)

    # # diagnosis
    print(f"{now()} # Diagnosis")
    if not conf.dry_run:
        encode_fails = check_encode_fails(encode_res)
        encode_fails.to_csv(conf.output_encode_fails_path, index=False)
        data_types.EncodeFails.validate(encode_fails)
        # check if there are efo terms ignored
        orig_ids = set([_["efo_id"] for _ in efo_terms])
        print(f"len orig {len(orig_ids)}")
        encode_ids = set([_["efo_id"] for _ in encode_res])
        print(f"len encode {len(encode_ids)}")
        diff = orig_ids.difference(encode_ids)
        print(f"diff {diff}")
        df = pd.DataFrame(efo_terms)
        df = df[df["efo_id"].isin(list(diff))]
        print(f"diff details {df}")

    if ray.is_initialized():
        ray.shutdown()


if __name__ == "__main__":
    main()
