from typing import Any, Dict, List

import requests
from loguru import logger

from .common_types import VectorEntItem


def query_vector_term(
    term_vector: List[float],
    es_url: str,
    score_threshold: float = 0.8,
) -> List[VectorEntItem]:
    def _format(item: Dict[str, Any]) -> VectorEntItem:
        res = item["_source"].copy()
        res["score"] = item["_score"]
        return res

    INDEX_NAME = "efo-vectors"
    url = f"{es_url}/{INDEX_NAME}/_knn_search"
    payload = {
        "knn": {
            "field": "vector",
            "query_vector": term_vector,
            "k": 3,
            "num_candidates": 10,
        },
        "_source": ["ent_id", "ent_term", "primary_term", "vector_term"],
    }
    r = requests.get(url, json=payload)
    try:
        r.raise_for_status()
    except Exception as e:
        logger.debug(str(e) + "\n" + r.text)
        raise
    results: List[VectorEntItem] = [
        _format(_)
        for _ in r.json()["hits"]["hits"]
        if _["_score"] >= score_threshold
    ]
    return results
