import requests
from fastapi import APIRouter
from loguru import logger

from app.resources import es_config, es_utils
from app.settings import ES_URL

router = APIRouter()


# TODO: replace embedding index with info index
# when info indices ready
@router.get("/entity/info/get")
async def get_entity_info_get(id: str, dictionary: str):
    """
    Get basic information for the entity of interest, by its id.

    - dictionary: hpo, ukbiobank, icd10, opengwas
    """
    assert dictionary in es_config.DICTIONARY_NAMES, logger.info(dictionary)
    query = es_utils.get_entity_query(id=id, dictionary=dictionary)
    logger.info(query)
    index_url = f"{ES_URL}/{es_config.DICTIONARY_INDICES[dictionary]}/_search"
    logger.info(index_url)
    r = requests.post(index_url, json=query)
    r.raise_for_status()
    response = r.json()
    sources = [_["_source"] for _ in response["hits"]["hits"]]
    assert len(sources) == 1, logger.info(sources)
    res = sources[0]
    return res


@router.get("/entity/info/search")
async def get_entity_info_search(q: str, dictionary: str):
    """
    Search an entity by text query on its label,
    and return the information of the corresponding entity
    including its embedding vector.

    - dictionary: hpo, ukbiobank, icd10, opengwas
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


@router.get("/entity/info/list")
async def get_entity_info_list(dictionary: str):
    """
    List all entities in a dictionary.
    NOTE: this is a preview of 5000 records and subject to change.
    """
    query = es_utils.doc_list(dictionary=dictionary)
    logger.info(query)
    index_url = f"{ES_URL}/{es_config.DICTIONARY_INDICES[dictionary]}/_search"
    logger.info(index_url)
    r = requests.get(index_url, json=query)
    r.raise_for_status()
    response = r.json()
    res = [_["_source"] for _ in response["hits"]["hits"]]
    return res
