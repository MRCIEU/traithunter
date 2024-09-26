import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Union

import pandas as pd
import simple_parsing
from loguru import logger
from pydash import py_
from simple_parsing import field

from analysis_funcs import paths

data_dir = paths.data_root
SUB_PROJ_NAME = "mvp-ontology-terms-2023-03"
OUTPUT_DIR = data_dir / "output" / SUB_PROJ_NAME


@dataclass
class Conf:
    dry_run: bool = field(alias="dry-run", action="store_true")
    trial: bool = field(action="store_true")
    trial_sample: int = 10
    input_distance_dir_path: Union[str, Path] = OUTPUT_DIR / "distance"
    output_pairwise_scores_path: Union[str, Path] = OUTPUT_DIR / "distance.csv"
    output_pairwise_scores_path_compressed: Union[str, Path] = (
        OUTPUT_DIR / "distance.csv.tar.gz"
    )


def make_conf() -> Conf:
    conf: Conf = simple_parsing.parse(Conf)
    conf.input_distance_dir_path = Path(conf.input_distance_dir_path)
    assert conf.input_distance_dir_path.exists(), conf.input_distance_dir_path
    conf.output_pairwise_scores_path = Path(conf.output_pairwise_scores_path)
    conf.output_pairwise_scores_path_compressed = Path(
        conf.output_pairwise_scores_path_compressed
    )
    if conf.trial:
        conf.output_pairwise_scores_path = OUTPUT_DIR / "distance_trial.csv"
    logger.info(f"conf {conf}")
    return conf


def format_pairwise(item: Dict[str, Any]):
    def _format_per_source(items_per_source: Dict[str, Any], id: str):
        res = [
            {
                "id_a": id,
                "id_b": _["ent_id"],
                "cosine_similarity": _["cosine_similarity"],
            }
            for _ in items_per_source["candidates"]
        ]
        return res

    id = item["id"]
    if item["results"] is None:
        logger.info(f"Results for {id} is None")
        return None
    nested_res = [
        _format_per_source(items_per_source=_, id=id) for _ in item["results"]
    ]
    res = py_.flatten(nested_res)
    return res


def make_pairwise_scores(
    input_file: Path, idx: int, total: int, conf: Conf
) -> pd.DataFrame:
    logger.info(f"#{idx}/{total} start processing file {input_file}")
    with input_file.open() as f:
        input_data = json.load(f)
    if conf.trial:
        input_data = input_data[: conf.trial_sample]
    nested_res = [format_pairwise(item=_) for _ in input_data]
    nested_res = [_ for _ in nested_res if _ is not None]
    flat_res = py_.flatten(nested_res)
    pairwise_df = pd.DataFrame(flat_res)
    logger.info(f"#{idx}/{total} finished processing file {input_file}")
    return pairwise_df


def main():
    conf = make_conf()

    distance_files = [
        _ for _ in conf.input_distance_dir_path.iterdir() if _.suffix == ".json"
    ]
    logger.info(f"files to process: {distance_files}")
    if not conf.dry_run:
        pairwise_scores: pd.DataFrame = pd.concat(
            [
                make_pairwise_scores(
                    input_file=_, idx=idx, total=len(distance_files), conf=conf
                )
                for idx, _ in enumerate(distance_files)
            ]
        ).reset_index(drop=True)
        pairwise_scores.to_csv(conf.output_pairwise_scores_path, index=False)
        if not conf.trial:
            pairwise_scores.to_csv(
                conf.output_pairwise_scores_path_compressed, index=False
            )


if __name__ == "__main__":
    main()
