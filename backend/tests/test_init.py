import requests

from app import settings


def test_elasticsearch():
    es_url = settings.es_url
    r = requests.get(es_url)
    assert r.ok, r.text
