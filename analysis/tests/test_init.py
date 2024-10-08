import requests

from analysis_funcs import paths
from analysis_funcs.settings import es_url


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
