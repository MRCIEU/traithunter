from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_vector_get():
    url = "/entity/vector/get"
    params = {
        "id": "ieu-b-40",
        "dictionary": "opengwas",
        "embedding_type": "bge",
    }
    r = client.get(url=url, params=params)
    r.raise_for_status()
    res = r.json()
    assert res is not None
    assert isinstance(res, list)


def test_get_vector_knn():
    url = "/entity/vector/knn"
    params = {
        "id": "ieu-b-40",
        "dictionary": "opengwas",
        "dictionary_to_query": "hpo",
        "embedding_type": "bge",
        "k": 30,
    }
    r = client.get(url=url, params=params)
    r.raise_for_status()
    res = r.json()
    assert res is not None
    assert isinstance(res, list)


def test_post_pairwise_similarity():
    url = "/entity/vector/pairwise-similarity"
    payload = {
        "entities": [
            {
                "entity_id": "ieu-b-40",
                "dictionary": "opengwas",
            },
            {
                "entity_id": "ieu-a-296",
                "dictionary": "opengwas",
            },
            {
                "entity_id": "ieu-a-7",
                "dictionary": "opengwas",
            },
            {
                "entity_id": "ieu-a-1102",
                "dictionary": "opengwas",
            },
        ],
        "embedding_type": "bge",
    }
    r = client.post(url=url, json=payload)
    r.raise_for_status()
    res = r.json()
    assert res is not None
    assert isinstance(res, list)
