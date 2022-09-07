from typing import Any, Dict


def efo_ents_query_by_ent_term_fuzzy(query: str) -> Dict[str, Any]:
    res = {"query": {"match": {"ent_term": {"query": query}}}}
    return res


def efo_ents_query_by_ent_term_exact(query: str) -> Dict[str, Any]:
    res = {"query": {"term": {"ent_term.raw": {"value": query}}}}
    return res


def efo_ents_query_by_ent_id(query: str) -> Dict[str, Any]:
    res = {"query": {"term": {"ent_id": {"value": query}}}}
    return res
