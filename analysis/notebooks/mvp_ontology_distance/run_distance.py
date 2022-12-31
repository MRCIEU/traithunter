import json
import math
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import numpy as np
import ray
import simple_parsing
from pydash import py_
from scipy.spatial import distance
from simple_parsing import field

from analysis_funcs import paths, now

import pandas as pd  # noqa
import janitor  # noqa

data_dir = paths.data_root
SUB_PROJ_NAME = "mvp-efo-terms-2022-12"
OUTPUT_DIR = data_dir / "output" / SUB_PROJ_NAME
INPUT_FILE = OUTPUT_DIR / "encode.json"


@dataclass
class Conf:
    input_file: Union[str, Path] = field(alias="input-file", default=INPUT_FILE)
    output_dir: Union[str, Path] = field(alias="output-dir", default=OUTPUT_DIR)
    dry_run: bool = field(alias="dry-run", action="store_true")
    trial: bool = field(action="store_true")
    num_workers: int = 12
    trial_sample: int = 500
    echo_step: int = 50000
    output_file: Optional[Union[str, Path]] = None


def make_conf() -> Conf:
    conf: Conf = simple_parsing.parse(Conf)
    conf.input_file = Path(conf.input_file)
    conf.output_dir = Path(conf.output_dir)
    assert conf.output_dir.exists(), conf.output_dir
    output_file_name = "distance.csv" if not conf.trial else "distance_trial.csv"
    conf.output_file = conf.output_dir / output_file_name
    mini_echo_step = 200
    if conf.trial:
        conf.echo_step = mini_echo_step
    print(conf)
    return conf


@ray.remote(num_cpus=1)
class DistanceCalc:
    def __init__(self, idx: int, vectors_df: pd.DataFrame, conf: Conf):
        self.idx = f"Actor {idx}"
        self.vectors_df = vectors_df
        self.conf = conf

    def calc_chunk(self, item_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        print(f"{now()} {self.idx}: Start to process {len(item_list)} items")
        vector_list = [
            {
                "id_a": _[0],
                "id_b": _[1],
                "vector_a": self.vectors_df.at[_[0], "term_vector"],
                "vector_b": self.vectors_df.at[_[1], "term_vector"],
            }
            for _ in item_list
        ]
        res = [self.calc(idx, len(vector_list), _) for idx, _ in enumerate(vector_list)]
        print(f"{now()} {self.idx}: Finish process")
        return res

    def calc(self, idx: int, total: int, item: Dict[str, Any]):
        echo_step = self.conf.echo_step
        if idx % echo_step == 0:
            print(f"{now()} {self.idx}: # {idx} / {total}")
        res = {
            "id_a": item["id_a"],
            "id_b": item["id_b"],
            "cosine_similarity": cosine_sim(item["vector_a"], item["vector_b"]),
        }
        return res


def cosine_sim(a: List[float], b: List[float]) -> float:
    def _invalid(vector: List[float]):
        res = not np.any(vector)
        return res
    if _invalid(a) or _invalid(b):
        return np.nan
    sim = 1 - distance.cosine(np.array(a), np.array(b))
    res = np.round(sim, 4)
    return res


def distance_main(vectors_df: pd.DataFrame, conf: Conf) -> pd.DataFrame:
    id_list = vectors_df.index.tolist()
    combs = list(combinations(id_list, 2))
    chunks = py_.chunk(combs, size=math.floor(len(combs) / conf.num_workers))
    print(f"len chunks {len(chunks)}")
    print(f"len chunks[0] {len(chunks[0])}")

    workers = [
        DistanceCalc.remote(idx=idx, vectors_df=vectors_df, conf=conf)  # type: ignore
        for idx, _ in enumerate(range(conf.num_workers))
    ]
    chunk_res = ray.get(
        [worker.calc_chunk.remote(chunks[idx]) for idx, worker in enumerate(workers)]
    )
    print(f"{now()} Finish nested results")
    res = pd.concat([
        pd.DataFrame(_)
        for _ in chunk_res
    ]).reset_index(drop=True)
    print(f"{now()} Finish flatten results")
    return res


def main():
    conf = make_conf()
    if ray.is_initialized():
        ray.shutdown()
    ray.init(num_cpus=conf.num_workers)
    print(ray.available_resources())

    with conf.input_file.open() as f:
        efo_vectors = json.load(f)
    print(f"len efo_vectors initialised {len(efo_vectors)}")
    if conf.trial:
        efo_vectors = efo_vectors[: conf.trial_sample]
    print(f"len efo_vectors to work on {len(efo_vectors)}")
    vectors_df = pd.DataFrame(efo_vectors).set_index("efo_id")

    if not conf.dry_run:
        print(f"{now()} Start processing")
        distance_res = distance_main(vectors_df, conf=conf)
        distance_res.to_csv(conf.output_file, index=False)

    print(f"{now()} All done")
    if ray.is_initialized():
        ray.shutdown()


if __name__ == "__main__":
    main()
