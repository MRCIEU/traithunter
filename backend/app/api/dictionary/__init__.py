from typing import List

from fastapi import APIRouter

from app.resources import es_config

router = APIRouter()


@router.get("/entity/dictionary/list")
async def get_entity_dictionary_list() -> List:
    res = es_config.DICTIONARY_NAMES
    return res


# async def get
