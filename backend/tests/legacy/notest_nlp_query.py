import pydantic
from common_funcs.common_types import VectorEntItem
from common_funcs.es_helpers import query_vector_term

from app.graphql_api.definitions.embed_term_defn import (
    resolver as embed_term_fn,
)
from app.settings import ES_URL


def test_query_vector_term():
    query = "body mass index"
    vector = embed_term_fn(query=query).results
    query_res = query_vector_term(term_vector=vector, es_url=ES_URL)
    model = pydantic.create_model_from_typeddict(VectorEntItem)
    assert model(**query_res[0])
