import requests

from funcs.settings import es_url


def test_elasticsearch():
    r = requests.get(es_url)
    assert r.ok, r.text
