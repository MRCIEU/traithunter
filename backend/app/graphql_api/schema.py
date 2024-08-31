import strawberry

from .definitions import (
    embed_term_defn,
    match_ent_defn,
    metadata_defn,
    ontology_ent_defn,
)


# NOTES: when import types must import the specific type, not the parent module
@strawberry.type
class Query:
    metadata: metadata_defn.Metadata = strawberry.field(
        resolver=metadata_defn.resolver,
        description=metadata_defn._docs,
    )
    embed_term: embed_term_defn.EmbedTermQuery = strawberry.field(
        resolver=embed_term_defn.resolver,
        description=embed_term_defn._docs,
    )
    match_ent: match_ent_defn.MatchEntQuery = strawberry.field(
        resolver=match_ent_defn.resolver,
        description=match_ent_defn._docs,
    )
    ontology_ent: ontology_ent_defn.OntologyEntQuery = strawberry.field(
        resolver=ontology_ent_defn.resolver,
        description=ontology_ent_defn._docs,
    )


schema = strawberry.Schema(query=Query)
