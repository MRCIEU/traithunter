import requests
from fastapi import APIRouter

from app.resources.es_config import INDEX_NAMES
from app.settings import ES_URL

router = APIRouter()


@router.get("/ping", response_model=bool)
def ping(dependencies: bool = True) -> bool:
    if not dependencies:
        return True
    else:
        r = requests.get(ES_URL)
        assert r.ok
        for k, v in INDEX_NAMES.items():
            url = f"{ES_URL}/{v}"
            r = requests.get(url)
        return True


@router.get("/utils/es-status")
def es_status():
    return INDEX_NAMES
