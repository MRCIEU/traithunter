import json
from dataclasses import dataclass

import pandas as pd
import requests
import simple_parsing
from loguru import logger
from simple_parsing import field

from analysis_funcs import es
from analysis_funcs.paths import data_root

from local_utils.es_config import INDEX_CONFIGS, INDEX_NAMES  # isort:skip

DATA_DIR_HPO = data_root / "source" / "hpo-2024-08"
DATA_DIR_UKBB = data_root / "source" / "ukbiobank-2024-08"
assert DATA_DIR_HPO.exists(), print(DATA_DIR_HPO)
assert DATA_DIR_UKBB.exists(), print(DATA_DIR_UKBB)


@dataclass
class Conf:
    dry_run: bool = field(alias="dry-run", action="store_true")
    rewrite: bool = field(alias="rewrite", action="store_true")
    es_url: str = "http://localhost:6360"
    trial: bool = field(alias="trial", action="store_true")
    trial_limit: int = 500


def make_conf() -> Conf:
    conf: Conf = simple_parsing.parse(Conf)
    logger.info(f"conf {conf}")
    return conf


def init(conf: Conf):
    r = requests.get(conf.es_url)
    assert r.ok, r.text


def index_ukbb_bge(conf: Conf):
    alias = "ukbiobank-bge"
    index_name = INDEX_NAMES[alias]
    if conf.trial:
        index_name = index_name + "--trial"
    index_config = INDEX_CONFIGS[alias]
    if es.index_exists(conf.es_url, index_name):
        if not conf.rewrite:
            logger.info(f"index {index_name} exists; skipping.")
            return None
        else:
            es.drop_index(conf.es_url, index_name)
    es.init_index(es_url=conf.es_url, index_name=index_name, config=index_config)

    data_path = DATA_DIR_UKBB / "embeddings_ukbb.json"
    assert data_path.exists(), print(data_path)

    logger.info(f"load {data_path}: start.")
    with data_path.open() as f:
        df = pd.DataFrame(json.load(f))
        logger.info(f"load {data_path}: done.")
        if conf.trial:
            df = df[: conf.trial_limit]
        df.info()

    df = df.rename(
        columns={
            "title": "label",
            "notes": "definition",
        }
    )

    logger.info(f"index {index_name}: start indexing.")
    es.bulk_index(
        es_url=conf.es_url, index_name=index_name, docs=df.to_dict(orient="records")
    )
    logger.info(f"index {index_name}: done indexing.")


def index_ukbb_llama3(conf: Conf):
    alias = "ukbiobank-llama3"
    index_name = INDEX_NAMES[alias]
    if conf.trial:
        index_name = index_name + "--trial"
    index_config = INDEX_CONFIGS[alias]
    if es.index_exists(conf.es_url, index_name):
        if not conf.rewrite:
            logger.info(f"index {index_name} exists; skipping.")
            return None
        else:
            es.drop_index(conf.es_url, index_name)
    es.init_index(es_url=conf.es_url, index_name=index_name, config=index_config)

    data_path = DATA_DIR_UKBB / "embeddings_ukbb_llama3.json"
    assert data_path.exists(), print(data_path)

    logger.info(f"load {data_path}: start.")
    with data_path.open() as f:
        df = pd.DataFrame(json.load(f))
        logger.info(f"load {data_path}: done.")
        if conf.trial:
            df = df[: conf.trial_limit]
        df.info()

    df = df.rename(
        columns={
            "title": "label",
            "notes": "definition",
        }
    ).assign(
        vector_title=lambda df: df["vector_title"].apply(lambda x: x[0]),
        vector_full=lambda df: df["vector_full_term"].apply(lambda x: x[0]),
    )

    logger.info(f"index {index_name}: start indexing.")
    es.bulk_index(
        es_url=conf.es_url, index_name=index_name, docs=df.to_dict(orient="records")
    )
    logger.info(f"index {index_name}: done indexing.")


def index_hpo_bge(conf: Conf):
    alias = "hpo-bge"
    index_name = INDEX_NAMES[alias]
    if conf.trial:
        index_name = index_name + "--trial"
    index_config = INDEX_CONFIGS[alias]
    if es.index_exists(conf.es_url, index_name):
        if not conf.rewrite:
            logger.info(f"index {index_name} exists; skipping.")
            return None
        else:
            es.drop_index(conf.es_url, index_name)
    es.init_index(es_url=conf.es_url, index_name=index_name, config=index_config)

    data_path = DATA_DIR_HPO / "embeddings_hpo.json"
    assert data_path.exists(), print(data_path)

    logger.info(f"load {data_path}: start.")
    with data_path.open() as f:
        df = pd.DataFrame(json.load(f))
        logger.info(f"load {data_path}: done.")
        if conf.trial:
            df = df[: conf.trial_limit]
        df.info()

    logger.info(f"index {index_name}: start indexing.")
    es.bulk_index(
        es_url=conf.es_url, index_name=index_name, docs=df.to_dict(orient="records")
    )
    logger.info(f"index {index_name}: done indexing.")


def index_hpo_llama3(conf: Conf):
    alias = "hpo-llama3"
    index_name = INDEX_NAMES[alias]
    if conf.trial:
        index_name = index_name + "--trial"
    index_config = INDEX_CONFIGS[alias]
    if es.index_exists(conf.es_url, index_name):
        if not conf.rewrite:
            logger.info(f"index {index_name} exists; skipping.")
            return None
        else:
            es.drop_index(conf.es_url, index_name)
    es.init_index(es_url=conf.es_url, index_name=index_name, config=index_config)

    data_path = DATA_DIR_HPO / "embeddings_hpo_llama3.json"
    assert data_path.exists(), print(data_path)

    logger.info(f"load {data_path}: start.")
    with data_path.open() as f:
        df = pd.DataFrame(json.load(f))
        logger.info(f"load {data_path}: done.")
        if conf.trial:
            df = df[: conf.trial_limit]
        df.info()

    df = df.assign(
        vector_title=lambda df: df["vector_title"].apply(lambda x: x[0]),
        vector_full=lambda df: df["vector_full_term"].apply(lambda x: x[0]),
    )

    logger.info(f"index {index_name}: start indexing.")
    es.bulk_index(
        es_url=conf.es_url, index_name=index_name, docs=df.to_dict(orient="records")
    )
    logger.info(f"index {index_name}: done indexing.")


def main():
    # init
    conf = make_conf()

    # init
    init(conf=conf)

    # ukbb_bge
    index_ukbb_bge(conf=conf)

    # ukbb_llama3
    index_ukbb_llama3(conf=conf)

    # hpo_bge
    index_hpo_bge(conf=conf)

    # hpo_llama3
    index_hpo_llama3(conf=conf)


if __name__ == "__main__":
    main()
