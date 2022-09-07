from typing import List

import strawberry
from common_funcs.es_helpers import query_vector_term

from app.settings import ES_URL

from . import common_types
from .embed_term_defn import resolver as embed_term_fn

_docs = "Match curated ontology entities by the query text"


@strawberry.type
class MatchEntMetadata:
    placeholder: None


@strawberry.type(description=_docs)
class MatchEntQuery:
    metadata: MatchEntMetadata
    results: List[common_types.VectorEnt]


def resolver(query: str) -> MatchEntQuery:
    vector = embed_term_fn(query=query).results
    metadata_res = MatchEntMetadata(placeholder=None)
    query_res = query_vector_term(term_vector=vector, es_url=ES_URL)
    match_res: List[common_types.VectorEnt] = [
        common_types.VectorEnt(**_) for _ in query_res
    ]
    res = MatchEntQuery(metadata=metadata_res, results=match_res)
    return res
