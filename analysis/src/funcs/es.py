import json
from typing import Any, Dict, List

import requests
from loguru import logger
from pydash import py_


def index_exists(es_url: str, index_name: str) -> bool:
    url = es_url + f"/{index_name}"
    r = requests.get(url)
    return r.ok


def drop_index(es_url: str, index_name: str) -> bool:
    url = es_url + f"/{index_name}"
    r = requests.get(url)
    if r.ok:
        logger.info(f"Drop index {index_name}")
        r = requests.delete(url)
    else:
        logger.info(f"{index_name} does not exist yet")
    return r.ok


def init_index(es_url: str, index_name: str, config: Dict[str, Any]) -> bool:
    url = es_url + f"/{index_name}"
    logger.info(f"Init index {index_name}")
    r = requests.put(url, json=config)
    r.raise_for_status()
    return r.ok


def bulk_index(
    es_url: str,
    index_name: str,
    docs: List[Dict[str, Any]],
    chunksize: int = 500,
    logger_step: int = 20,
):
    docs_chunks = py_.chunk(docs, size=chunksize)
    print(f"split {len(docs)} into {len(docs_chunks)} chunks")
    for idx, chunk in enumerate(docs_chunks):
        if idx % logger_step == 0:
            print(f"# chunk {idx} / {len(docs_chunks)}")
        index_chunk(es_url, index_name, chunk)


def index_chunk(es_url: str, index_name: str, docs: List[Dict[str, Any]]):
    index_url = es_url + f"/{index_name}" + "/_bulk"
    headers = {"Content-Type": "application/x-ndjson", "charset": "UTF-8"}
    delim: Dict[str, Any] = {"index": {}}
    arr = []
    for _ in docs:
        arr.append(delim)
        arr.append(_)
    payload = "\n".join([json.dumps(_) for _ in arr]) + "\n"
    r = requests.post(index_url, data=payload, headers=headers)
    r.raise_for_status()
