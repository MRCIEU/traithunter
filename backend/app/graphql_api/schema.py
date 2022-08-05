import strawberry

from .definitions.metadata import Metadata
from .definitions.search_ent import SearchEnt
from .resolvers.metadata import get_metadata
from .resolvers.search_ent import search_ent_fn


@strawberry.type
class Query:
    metadata: Metadata = strawberry.field(resolver=get_metadata)
    search_ent: SearchEnt = strawberry.field(resolver=search_ent_fn)


schema = strawberry.Schema(query=Query)
