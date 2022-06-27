import requests

from funcs.settings import es_url
from funcs import paths


def test_elasticsearch():
    r = requests.get(es_url)
    assert r.ok, r.text


def test_input_data():
    print("efo")
    efo_path = paths.data["efo"]
    assert efo_path.exists(), efo_path

def test_input_models():
    print("scispacy lg")
    scispacy_lg_path = paths.models["scispacy_lg"]
    assert scispacy_lg_path.exists(), scispacy_lg_path
