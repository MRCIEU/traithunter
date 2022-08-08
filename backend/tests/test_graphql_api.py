import numpy as np
from starlette.testclient import TestClient

from app.main import app


def test_embed_term():
    query = """query {
        embedTerm(query: "body mass index") {
          metadata {
            modelName
            vectorLength
          }
          results
        }
    }
    """
    payload = {"query": query}
    with TestClient(app) as client:
        r = client.post("/graphql", json=payload)
    print(r.json())
    assert r.ok
    vector = r.json()["data"]["embedTerm"]["results"]
    assert len(vector) > 0
    empty_vector = np.equal(np.sum(vector), 0)
    assert not empty_vector


def test_match_ent():
    query = """query {
        matchEnt(query: 'body mass index') {
          metadata
          results
        }
    }
    """
    payload = {"query": query}
    with TestClient(app) as client:
        r = client.post("/graphql", json=payload)
    print(r.json())
    assert r.ok
