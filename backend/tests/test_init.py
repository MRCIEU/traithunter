import requests

from app import settings


def test_elasticsearch():
    es_url = settings.ES_URL
    r = requests.get(es_url)
    assert r.ok, r.text


def test_model_path():
    model_path = settings.SCISPACY_LG_PATH
    assert model_path.exists(), model_path
