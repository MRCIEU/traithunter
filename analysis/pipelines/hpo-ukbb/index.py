from dataclasses import dataclass

import pandas as pd
import requests
import simple_parsing
from elasticsearch import Elasticsearch, helpers
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
    trial_limit: int = 50


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
    df = pd.read_json(data_path)
    df.info()
    if conf.trial:
        df = df[: conf.trial_limit]

    df = df.rename(
        columns={
            "title": "label",
            "notes": "description",
            "vector_full_term": "vector_full",
        }
    )

    def generate_docs():
        for idx, row in df.iterrows():
            yield {
                "_index": index_name,
                "id": row["id"],
                "label": row["label"],
                "description": row["description"],
                "vector_title": row["vector_title"],
                "vector_full": row["vector_full"],
            }

    if not conf.dry_run:
        logger.info(f"index {index_name}: start indexing.")
        client = Elasticsearch(conf.es_url)
        client.info()
        helpers.bulk(client, generate_docs())
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
    df = pd.read_json(data_path)
    df.info()
    if conf.trial:
        df = df[: conf.trial_limit]

    df = df.rename(columns={"title": "label", "notes": "description"}).assign(
        vector_title=lambda df: df["vector_title"].apply(lambda x: x[0]),
        vector_full=lambda df: df["vector_full_term"].apply(lambda x: x[0]),
    )
    df.info()
    print(df.head())

    def generate_docs():
        for idx, row in df.iterrows():
            yield {
                "_index": index_name,
                "id": row["id"],
                "label": row["label"],
                "description": row["description"],
                "vector_title": row["vector_title"],
                "vector_full": row["vector_full"],
            }

    if not conf.dry_run:
        logger.info(f"index {index_name}: start indexing.")
        client = Elasticsearch(conf.es_url)
        client.info()
        helpers.bulk(client, generate_docs())
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
    df = pd.read_json(data_path)
    df.info()
    if conf.trial:
        df = df[: conf.trial_limit]

    df = df.rename(
        columns={"vector_full_term": "vector_full", "definition": "description"}
    )

    def generate_docs():
        for idx, row in df.iterrows():
            yield {
                "_index": index_name,
                "id": row["id"],
                "hpo_id": row["hpo_id"],
                "label": row["label"],
                "description": row["description"],
                "type": row["type"],
                "vector_title": row["vector_title"],
                "vector_full": row["vector_full"],
            }

    if not conf.dry_run:
        logger.info(f"index {index_name}: start indexing.")
        client = Elasticsearch(conf.es_url)
        client.info()
        helpers.bulk(client, generate_docs())
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
    df = pd.read_json(data_path)
    df.info()
    if conf.trial:
        df = df[: conf.trial_limit]

    df = df.rename(
        columns={"vector_full_term": "vector_full", "definition": "description"}
    ).assign(
        vector_title=lambda df: df["vector_title"].apply(lambda x: x[0]),
        vector_full=lambda df: df["vector_full"].apply(lambda x: x[0]),
    )

    def generate_docs():
        for idx, row in df.iterrows():
            yield {
                "_index": index_name,
                "id": row["id"],
                "hpo_id": row["hpo_id"],
                "label": row["label"],
                "description": row["description"],
                "type": row["type"],
                "vector_title": row["vector_title"],
                "vector_full": row["vector_full"],
            }

    if not conf.dry_run:
        logger.info(f"index {index_name}: start indexing.")
        client = Elasticsearch(conf.es_url)
        client.info()
        helpers.bulk(client, generate_docs())
        logger.info(f"index {index_name}: done indexing.")


def main():
    conf = make_conf()
    init(conf=conf)

    index_ukbb_bge(conf=conf)
    index_ukbb_llama3(conf=conf)
    index_hpo_bge(conf=conf)
    index_hpo_llama3(conf=conf)


if __name__ == "__main__":
    main()
