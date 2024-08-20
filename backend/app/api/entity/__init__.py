import requests

from fastapi import APIRouter
from loguru import logger

from app.settings import ES_URL
from app.resources import es_utils, es_config

router = APIRouter()

@router.get("/entity/get")
def get_entity_get(id: str, dictionary: str):
    """
    dictionary: hpo, ukbiobank, icd10
    """
    assert dictionary in es_config.DICTIONARY_NAMES, logger.info(dictionary)
    query = es_utils.get_entity_query(id=id, dictionary=dictionary)
    logger.info(query)
    index_url = f"{ES_URL}/{es_config.DICTIONARY_INDICES[dictionary]}/_search"
    logger.info(index_url)
    r = requests.post(index_url, json=query)
    r.raise_for_status()
    response = r.json()
    res = response["hits"]["hits"]
    return res


@router.get("/entity/search")
def get_entity_search(q: str, dictionary: str):
    """
    dictionary: hpo, ukbiobank, icd10
    """
    assert dictionary in es_config.DICTIONARY_NAMES, logger.info(dictionary)
    query = es_utils.search_entity_query(q=q, dictionary=dictionary)
    logger.info(query)
    index_url = f"{ES_URL}/{es_config.DICTIONARY_INDICES[dictionary]}/_search"
    logger.info(index_url)
    r = requests.post(index_url, json=query)
    r.raise_for_status()
    response = r.json()
    res = [_["_source"] for _ in response["hits"]["hits"]]
    return res


@router.get("/entity/knn")
def get_entity_knn(id: str, dictionary: str, dictionary_to_query: str, k: int = 15):
    """
    k-Nearest Neighbours search by high-dimensional vectors
    dictionary: hpo, ukbiobank, icd10
    """
    assert dictionary in es_config.DICTIONARY_NAMES, logger.info(dictionary)
    assert dictionary_to_query in es_config.DICTIONARY_NAMES, logger.info(dictionary_to_query)

    # get vectors
    query = es_utils.get_entity_vector_query(id=id, dictionary=dictionary)
    logger.info(query)
    index_url = f"{ES_URL}/{es_config.DICTIONARY_INDICES[dictionary]}/_search"
    logger.info(index_url)
    r = requests.post(index_url, json=query)
    r.raise_for_status()
    response = r.json()
    query_vector = response["hits"]["hits"][0]["_source"]["vector_title"]

    # get knn
    query = es_utils.knn_query(query_vector=query_vector, dictionary=dictionary_to_query, k=k)
    # TODO: llama and bge
    index_url = f"{ES_URL}/{es_config.DICTIONARY_INDICES[dictionary_to_query]}/_search"
    logger.info(index_url)
    r = requests.post(index_url, json=query)
    r.raise_for_status()
    response = r.json()
    res = [
        {
            "item": _["_source"],
            "score": _["_score"]
        }
        for _ in response["hits"]["hits"]
    ]
    return res
