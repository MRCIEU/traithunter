import strawberry

from .definitions.embed_term import EmbedTerm
from .definitions.match_ent import MatchEnt
from .definitions.metadata import Metadata
from .resolvers.embed_term import embed_term_fn
from .resolvers.match_ent import match_ent_fn
from .resolvers.metadata import get_metadata


@strawberry.type
class Query:
    metadata: Metadata = strawberry.field(resolver=get_metadata)
    embed_term: EmbedTerm = strawberry.field(resolver=embed_term_fn)
    match_ent: MatchEnt = strawberry.field(resolver=match_ent_fn)
    # TODO: list terms by ontology, paginatable
    # ontology_ent(id, exact_term, fuzzy_term, limit)


schema = strawberry.Schema(query=Query)
