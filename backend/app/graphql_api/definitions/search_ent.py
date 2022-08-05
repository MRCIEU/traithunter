from typing import List

import strawberry


@strawberry.type
class SearchEntMetadata:
    placeholder: None


@strawberry.type
class SearchEntItem:
    placeholder: None


@strawberry.type
class SearchEnt:
    metadata: SearchEntMetadata
    results: List[SearchEntItem]
