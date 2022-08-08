from typing import List

import strawberry

_docs = "Metadata information"


@strawberry.type(description=_docs)
class Metadata:
    description: str
    ontologies: List[str]
