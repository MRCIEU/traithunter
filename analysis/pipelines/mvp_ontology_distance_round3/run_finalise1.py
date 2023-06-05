import sqlite3
from dataclasses import dataclass
from pathlib import Path

import requests
import pandas as pd
import simple_parsing
from loguru import logger
from simple_parsing import field

from analysis_funcs import paths, settings
import local_utils


data_dir = paths.data_root
SUB_PROJ_NAME = "mvp-ontology-terms-2023-03"
OUTPUT_DIR = data_dir / "output" / SUB_PROJ_NAME


@dataclass
class Conf:
    dry_run: bool = field(alias="dry-run", action="store_true")
    trial: bool = field(action="store_true")
    overwrite: bool = field(action="store_true")
    trial_sample: int = 10
    es_url: str = settings.es_url
    input_terms_path: Path = OUTPUT_DIR / "clean_terms.csv"
    input_pairwise_scores_path: Path = OUTPUT_DIR / "distance.csv"
    output_pairwise_scores_db_path: Path = OUTPUT_DIR / "distance.db"
    output_encodings_db_path: Path = OUTPUT_DIR / "encodings.db"


def make_conf() -> Conf:
    conf: Conf = simple_parsing.parse(Conf)
    assert conf.input_pairwise_scores_path.exists(), conf.input_pairwise_scores_path
    if conf.trial:
        conf.output_pairwise_scores_db_path = OUTPUT_DIR / "distance_trial.db"
        conf.output_encodings_db_path = OUTPUT_DIR / "encodings_trial.db"
    return conf


def gen_target_vector_payload(target_id):
    res = {
        "query": {
            "term": {"ent_id": target_id},
        },
        "_source": ["ent_id", "vector"],
    }
    return res


def get_target_vector(target_id: str, source: str, es_url: str):
    index_name = local_utils.get_es_index_for_source(source=source, trial=False)
    url = es_url + f"/{index_name}/_search"
    payload = gen_target_vector_payload(target_id=target_id)
    r = requests.get(url, json=payload)
    r.raise_for_status
    results = r.json()["hits"]["hits"]
    if len(results) > 0:
        res = results[0]["_source"]
    else:
        res = None
    return res


def get_encodings(terms_df: pd.DataFrame, conf: Conf) -> pd.DataFrame:
    if conf.trial:
        terms_df = terms_df[:300]
    vector_res = [
        get_target_vector(target_id=_["id"], source=_["source"], es_url=conf.es_url)
        for _ in terms_df.to_dict(orient="records")
    ]
    res = pd.DataFrame([_ for _ in vector_res if _ is not None])
    res = res.rename(columns={"ent_id": "id"}).assign(
        vector=lambda df: df["vector"].apply(lambda x: str(x))
    )
    return res


def main():
    conf = make_conf()
    terms_df = pd.read_csv(conf.input_terms_path)
    if not conf.overwrite and conf.output_pairwise_scores_db_path.exists():
        logger.info(f"db {conf.output_pairwise_scores_db_path} exist skips")
    else:
        logger.info(f"write to db {conf.output_pairwise_scores_db_path}")
        pairwise_df = pd.read_csv(conf.input_pairwise_scores_path)
        sample_df = pairwise_df if not conf.trial else pairwise_df[:3000]
        con = sqlite3.connect(conf.output_pairwise_scores_db_path)
        logger.info(f"Write 'terms' table")
        terms_df.set_index("id").to_sql(
            name="terms", con=con, if_exists="replace", index=True
        )
        logger.info(f"Write 'distance' table")
        sample_df.set_index(["id_a", "id_b"]).to_sql(
            name="distance",
            con=con,
            if_exists="replace",
            index=True,
            index_label=["id_a", "id_b"],
        )
    if not conf.overwrite and conf.output_encodings_db_path.exists():
        logger.info(f"db {conf.output_encodings_db_path} exist skips")
    else:
        logger.info(f"Write to db {conf.output_encodings_db_path}")
        con = sqlite3.connect(conf.output_encodings_db_path)
        encodings_df = get_encodings(terms_df=terms_df, conf=conf)
        encodings_df.set_index("id").to_sql(
            name="encodings", con=con, if_exists="replace", index=True
        )


if __name__ == "__main__":
    main()
