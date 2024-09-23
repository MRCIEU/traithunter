import requests

from analysis_funcs import settings

ES_URL = settings.es_url


def test_primary_term_expect_found():
    term = (
        "here is a very long trait_label regarding cervical cancer and many other stuff"
    )

    index_name = "efo-ents"
    url = ES_URL + f"/{index_name}/_search"
    payload = {"query": {"match": {"ent_term.raw": term}}}
    r = requests.get(url, json=payload)
    r.raise_for_status()
    results = r.json()["hits"]["hits"]
    # Expect ["cancer", "cervix cancer"], NOTE: should then filter cancer out
    # in post processing
    assert len(results) == 2, [_["_source"]["ent_term"] for _ in results]


def test_primary_term_expect_not_found():
    term = "here is a very long trait_label on Nergigante that is not supposed to exist"

    index_name = "efo-ents"
    url = ES_URL + f"/{index_name}/_search"
    payload = {"query": {"match": {"ent_term.raw": term}}}
    r = requests.get(url, json=payload)
    r.raise_for_status()
    results = r.json()["hits"]["hits"]
    assert len(results) == 0, [_["_source"]["ent_term"] for _ in results]


def test_synonym_term_expect_found():
    term = (
        "here is a very long trait_label regarding cervical cancer and many other stuff"
    )

    index_name = "efo-vectors"
    url = ES_URL + f"/{index_name}/_search"
    payload = {"query": {"match": {"vector_term.raw": term}}}
    r = requests.get(url, json=payload)
    r.raise_for_status()
    results = r.json()["hits"]["hits"]
    assert len(results) == 2, [_["_source"]["vector_term"] for _ in results]


def test_synonym_term_expect_not_found():
    term = "here is a very long term_label on Gore-Magala that is not supposed to exist"

    index_name = "efo-vectors"
    url = ES_URL + f"/{index_name}/_search"
    payload = {"query": {"match": {"vector_term.raw": term}}}
    r = requests.get(url, json=payload)
    r.raise_for_status()
    results = r.json()["hits"]["hits"]
    assert len(results) == 0, [_["_source"]["vector_term"] for _ in results]
