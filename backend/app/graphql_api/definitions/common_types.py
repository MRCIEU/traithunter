from typing import List, Optional

import strawberry


@strawberry.type
class VectorEnt:
    ent_id: str
    ent_term: str
    vector_term: str
    primary_term: bool
    score: float


@strawberry.type
class OntologyEnt:
    ent_id: str
    ent_term: str
    description: Optional[str]
    synonyms: Optional[List[str]]
