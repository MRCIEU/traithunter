from typing import List

import strawberry

_docs = "Embed (encode) query text into vector"


@strawberry.type
class EmbedTermMetadata:
    vector_length: int
    model_name: str


@strawberry.type(description=_docs)
class EmbedTerm:
    metadata: EmbedTermMetadata
    results: List[float]
