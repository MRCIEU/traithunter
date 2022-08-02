import requests
from starlette.testclient import TestClient

from app import settings
from app.main import app


def test_ping():
    with TestClient(app) as client:
        r = client.get("/ping")
    assert r.ok


def test_graphql_query_user():
    query = """query {
        user {
          name
          age
        }
    }
    """
    payload = {"query": query}
    with TestClient(app) as client:
        r = client.post("/graphql", json=payload)
    print(r.json())
    assert r.ok


def test_elasticsearch():
    es_url = settings.es_url
    r = requests.get(es_url)
    assert r.ok, r.text
