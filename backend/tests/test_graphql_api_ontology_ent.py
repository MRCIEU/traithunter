from string import Template

from starlette.testclient import TestClient

from app.graphql_api.definitions import ontology_ent_defn
from app.main import app

ENT_ID = "http://www.orpha.net/ORDO/Orphanet_209203"
ENT_TERM_FUZZY = "cancer"
ENT_TERM_EXACT = "cervical cancer"


def test_query_by_ent_id_fn():
    query = ENT_ID
    res = ontology_ent_defn._query_by_ent_id(query=query)
    print(res)
    assert len(res) > 0


def test_query_by_ent_term_fuzzy_fn():
    query = ENT_TERM_FUZZY
    res = ontology_ent_defn._query_by_ent_term_fuzzy(query=query)
    print(res)
    assert len(res) > 0


def test_query_by_ent_term_exact_fn():
    query = ENT_TERM_EXACT
    res = ontology_ent_defn._query_by_ent_term_exact(query=query)
    print(res)
    assert len(res) > 0


def test_query_by_ent_id_api():
    ent_id = ENT_ID
    template = Template(
        """query {
        ontologyEnt(entId: "$ent_id") {
            results {
              entId
              entTerm
              description
              synonyms
            }
        }
    }
    """
    )
    query = template.substitute(ent_id=ent_id)
    print(query)
    payload = {"query": query}
    with TestClient(app) as client:
        r = client.post("/graphql", json=payload)
    print(r.json())
    assert r.ok
    results = r.json()["data"]["ontologyEnt"]["results"]
    print(results)
    assert len(results) > 0


def test_query_by_ent_term_exact():
    ent_term = ENT_TERM_EXACT
    template = Template(
        """query {
        ontologyEnt(entTerm: "$ent_term", fuzzy: false) {
            results {
              entId
              entTerm
              description
              synonyms
            }
        }
    }
    """
    )
    query = template.substitute(ent_term=ent_term)
    print(query)
    payload = {"query": query}
    with TestClient(app) as client:
        r = client.post("/graphql", json=payload)
    print(r.json())
    assert r.ok
    results = r.json()["data"]["ontologyEnt"]["results"]
    print(results)
    assert len(results) > 0


def test_query_by_ent_term_fuzzy():
    ent_term = ENT_TERM_FUZZY
    template = Template(
        """query {
        ontologyEnt(entTerm: "$ent_term", fuzzy: true) {
            results {
              entId
              entTerm
              description
              synonyms
            }
        }
    }
    """
    )
    query = template.substitute(ent_term=ent_term)
    print(query)
    payload = {"query": query}
    with TestClient(app) as client:
        r = client.post("/graphql", json=payload)
    print(r.json())
    assert r.ok
    results = r.json()["data"]["ontologyEnt"]["results"]
    print(results)
    assert len(results) > 0
