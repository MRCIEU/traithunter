from typing import Any, Dict, List, Optional

import requests
import strawberry
from common_funcs import es_query_templates
from loguru import logger

from app.settings import ES_URL

from . import common_types

_docs = "Retrieve ontology entity by its `ent_id` or `ent_term`"


@strawberry.type(description=_docs)
class OntologyEntQuery:
    results: List[common_types.OntologyEnt]


PlainResults = List[Dict[str, Any]]


def resolver(
    ent_id: Optional[str] = None,
    ent_term: Optional[str] = None,
    fuzzy: bool = False,
) -> OntologyEntQuery:
    """
    `ent_id` when specified will be prioritised over `ent_term`,
    fuzzy only works with ent_term
    """
    plain_results: PlainResults = []
    if ent_id is not None:
        plain_results = _query_by_ent_id(query=ent_id)
    elif ent_term is not None:
        if fuzzy:
            plain_results = _query_by_ent_term_fuzzy(query=ent_term)
        else:
            plain_results = _query_by_ent_term_exact(query=ent_term)
    results = [common_types.OntologyEnt(**_) for _ in plain_results]
    res = OntologyEntQuery(results=results)
    return res


def _query_by_ent_id(query: str) -> PlainResults:
    payload = es_query_templates.efo_ents_query_by_ent_id(query=query)
    index_name = "efo-ents"
    url = f"{ES_URL}/{index_name}/_search"
    r = requests.get(url, json=payload)
    try:
        r.raise_for_status()
    except Exception as e:
        logger.debug(str(e) + "\n" + r.text)
        raise
    res = [_format(_) for _ in r.json()["hits"]["hits"]]
    return res


def _query_by_ent_term_exact(query: str) -> PlainResults:
    payload = es_query_templates.efo_ents_query_by_ent_term_exact(query=query)
    index_name = "efo-ents"
    url = f"{ES_URL}/{index_name}/_search"
    r = requests.get(url, json=payload)
    try:
        r.raise_for_status()
    except Exception as e:
        logger.debug(str(e) + "\n" + r.text)
        raise
    res = [_format(_) for _ in r.json()["hits"]["hits"]]
    return res


def _query_by_ent_term_fuzzy(query: str) -> PlainResults:
    payload = es_query_templates.efo_ents_query_by_ent_term_fuzzy(query=query)
    index_name = "efo-ents"
    url = f"{ES_URL}/{index_name}/_search"
    r = requests.get(url, json=payload)
    try:
        r.raise_for_status()
    except Exception as e:
        logger.debug(str(e) + "\n" + r.text)
        raise
    res = [_format(_) for _ in r.json()["hits"]["hits"]]
    return res


def _format(item: Dict[str, Any]) -> Dict[str, Any]:
    res = item["_source"]
    return res
