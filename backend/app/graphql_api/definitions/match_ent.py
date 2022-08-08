from typing import List

import strawberry

_docs = "Match curated ontology entities by the query text"


@strawberry.type
class MatchEntMetadata:
    placeholder: None


@strawberry.type
class VectorEntItem:
    ent_id: str
    ent_term: str
    vector_term: str
    primary_term: bool
    score: float


@strawberry.type(description=_docs)
class MatchEnt:
    metadata: MatchEntMetadata
    results: List[VectorEntItem]
