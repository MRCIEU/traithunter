from typing_extensions import TypedDict


class VectorEntItem(TypedDict):
    ent_id: str
    ent_term: str
    vector_term: str
    primary_term: bool
    score: float
