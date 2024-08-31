import requests
from fastapi import APIRouter
from loguru import logger

from app.resources import es_config, es_utils
from app.settings import ES_URL

router = APIRouter()


@router.get("/entity/vector/get")
async def get_vector_get(
    id: str, dictionary: str, embedding_type: str = "bge"
):
    """
    Get the embedding vector for the entity of interest, by its id.

    - dictionary: hpo, ukbiobank, icd10, opengwas
    """
    assert dictionary in es_config.DICTIONARY_NAMES, logger.info(dictionary)

    # get vectors
    query = es_utils.get_entity_vector_query(id=id, dictionary=dictionary)
    logger.info(query)
    embedding_index = es_config.INDICES[dictionary][embedding_type]
    index_url = f"{ES_URL}/{embedding_index}/_search"
    logger.info(index_url)
    r = requests.post(index_url, json=query)
    r.raise_for_status()
    response = r.json()
    query_vector = response["hits"]["hits"][0]["_source"]["vector_title"]
    res = query_vector
    return res


@router.get("/entity/vector/knn")
async def get_vector_knn(
    id: str,
    dictionary: str,
    dictionary_to_query: str,
    k: int = 15,
    embedding_type: str = "bge",
):
    """
    k-Nearest Neighbours search by embedding vectors.

    - dictionary: hpo, ukbiobank, icd10, opengwas
    - embedding_type: bge (dim: 768), llama3 (dim: 4096)
    """
    assert dictionary in es_config.DICTIONARY_NAMES, logger.info(dictionary)
    assert dictionary_to_query in es_config.DICTIONARY_NAMES, logger.info(
        dictionary_to_query
    )
    assert embedding_type in es_config.EMBEDDING_TYPE, logger.info(
        embedding_type
    )

    query_vector = await get_vector_get(
        id=id, dictionary=dictionary, embedding_type=embedding_type
    )

    # get knn
    query = es_utils.knn_query(
        query_vector=query_vector, dictionary=dictionary_to_query, k=k
    )
    embedding_index_to_query = es_config.INDICES[dictionary_to_query][
        embedding_type
    ]
    index_url = f"{ES_URL}/{embedding_index_to_query}/_search"
    logger.info(index_url)
    r = requests.post(index_url, json=query)
    r.raise_for_status()
    response = r.json()
    res = [
        {"item": _["_source"], "score": _["_score"]}
        for _ in response["hits"]["hits"]
    ]
    return res
