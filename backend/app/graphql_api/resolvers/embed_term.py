from typing import List

from app.funcs.nlp import get_scispacy_lg, scispacy_encode
from app.settings import SCISPACY_LG_NAME

from ..definitions import embed_term as embed_term_defn


def embed_term_fn(query: str) -> embed_term_defn.EmbedTerm:
    nlp_model = get_scispacy_lg()
    embed_res: List[float] = scispacy_encode(text=query, nlp_model=nlp_model)
    metadata_res = embed_term_defn.EmbedTermMetadata(
        model_name=SCISPACY_LG_NAME, vector_length=len(embed_res)
    )
    res = embed_term_defn.EmbedTerm(metadata=metadata_res, results=embed_res)
    return res
