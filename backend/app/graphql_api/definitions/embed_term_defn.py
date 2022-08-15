from typing import List

import strawberry

from app.funcs.nlp import get_scispacy_lg, scispacy_encode
from app.settings import SCISPACY_LG_NAME

_docs = "Embed (encode) query text into vector"


@strawberry.type
class EmbedTermMetadata:
    vector_length: int
    model_name: str


@strawberry.type(description=_docs)
class EmbedTermQuery:
    metadata: EmbedTermMetadata
    results: List[float] = strawberry.field(
        description="Embedding vector as a list of floats"
    )


def resolver(query: str) -> EmbedTermQuery:
    nlp_model = get_scispacy_lg()
    embed_res: List[float] = scispacy_encode(text=query, nlp_model=nlp_model)
    metadata_res = EmbedTermMetadata(
        model_name=SCISPACY_LG_NAME, vector_length=len(embed_res)
    )
    res = EmbedTermQuery(metadata=metadata_res, results=embed_res)
    return res
