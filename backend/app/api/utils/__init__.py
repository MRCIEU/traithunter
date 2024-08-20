import requests
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.settings import ES_URL
from app.resources.es_config import INDEX_NAMES

templates = Jinja2Templates(directory="templates")
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


@router.get("/schema", response_class=HTMLResponse, include_in_schema=False)
async def graphql_schema(request: Request):
    return templates.TemplateResponse(
        "index.html", context={"request": request}
    )
