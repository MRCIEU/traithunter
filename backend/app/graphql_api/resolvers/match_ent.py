from typing import List

from common_funcs.es_helpers import query_vector_term

from app.settings import ES_URL

from ..definitions import match_ent as defn
from .embed_term import embed_term_fn


def match_ent_fn(query: str) -> defn.MatchEnt:
    vector = embed_term_fn(query=query).results
    metadata_res = defn.MatchEntMetadata(placeholder=None)
    query_res = query_vector_term(term_vector=vector, es_url=ES_URL)
    match_res: List[defn.VectorEntItem] = [
        defn.VectorEntItem(**_) for _ in query_res
    ]
    res = defn.MatchEnt(metadata=metadata_res, results=match_res)
    return res
