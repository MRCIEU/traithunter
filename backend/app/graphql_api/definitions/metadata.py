from typing import List

import strawberry


@strawberry.type
class Metadata:
    description: str
    ontologies: List[str]
