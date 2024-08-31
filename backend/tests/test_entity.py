from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_entity_info_get():
    url = "/entity/info/get"
    params = {"id": "ieu-b-40", "dictionary": "opengwas"}
    r = client.get(url=url, params=params)
    r.raise_for_status()
    assert r.json() is not None


def test_entity_info_search():
    url = "/entity/info/search"
    params = {
        "q": "body mass",
        "dictionary": "opengwas",
    }
    r = client.get(url=url, params=params)
    r.raise_for_status()
    assert len(r.json()) > 0
