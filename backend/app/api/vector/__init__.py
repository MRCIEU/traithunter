from itertools import permutations
from typing import List

import numpy as np
import requests
from fastapi import APIRouter
from loguru import logger
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity

from app.resources import es_config, es_utils
from app.settings import ES_URL

router = APIRouter()


class Entity(BaseModel):
    entity_id: str
    dictionary: str


class PairwiseInput(BaseModel):
    entities: List[Entity]
    # TODO: change this to enum of embedding types
    embedding_type: str


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


@router.post("/entity/vector/pairwise-similarity")
async def post_pairwise_similarity(input: PairwiseInput):
    # TODO: formalise validation
    assert len(input.entities) <= 15
    params = [
        {
            "id": _.entity_id,
            "dictionary": _.dictionary,
            "embedding_type": input.embedding_type,
        }
        for _ in input.entities
    ]
    logger.info(params)
    vectors = [
        await get_vector_get(
            id=_["id"],
            dictionary=_["dictionary"],
            embedding_type=_["embedding_type"],
        )
        for _ in params
    ]
    cosine_res = cosine_similarity(np.array(vectors))
    perm = permutations(range(len(params)), 2)
    res = [
        {
            "entity_a": {
                "id": params[_[0]]["id"],
                "dictionary": params[_[0]]["dictionary"],
            },
            "entity_b": {
                "id": params[_[1]]["id"],
                "dictionary": params[_[1]]["dictionary"],
            },
            "similarity_score": float(cosine_res[_[0], _[1]]),
        }
        for _ in list(perm)
    ]
    return res
