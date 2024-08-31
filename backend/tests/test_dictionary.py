from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_entity_dictionary_list():
    url = "/entity/dictionary/list"
    r = client.get(url=url)
    r.raise_for_status()
    assert len(r.json()) > 0
