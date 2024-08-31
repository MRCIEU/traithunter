from typing import List

import requests
from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.resources import es_config
from app.settings import ES_URL

router = APIRouter()


@router.get("/entity/dictionary/list")
async def get_entity_dictionary_list() -> List:
    res = es_config.DICTIONARY_NAMES
    return res


@cache()
@router.get("/entity/dictionary/length")
async def get_entity_dictionary_length(dictionary: str) -> int:
    assert dictionary in es_config.DICTIONARY_NAMES
    dictionary_index = es_config.DICTIONARY_INDICES[dictionary]
    url = f"{ES_URL}/{dictionary_index}/_stats"
    r = requests.get(url)
    r.raise_for_status()
    response = r.json()
    res = response["indices"][dictionary_index]["primaries"]["docs"]["count"]
    return res
