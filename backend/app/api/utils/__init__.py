from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/ping", response_model=bool)
def ping(dependencies: bool = True) -> bool:
    if not dependencies:
        return True
    else:
        # status: Dict[str, bool] = check_component_status(
        #     config=config, verbose=True
        # )
        # res = sum([_ for _ in status.values()]) == len(status.values())
        res = True
        return res


@router.get("/schema", response_class=HTMLResponse, include_in_schema=False)
async def graphql_schema(request: Request):
    return templates.TemplateResponse(
        "index.html", context={"request": request}
    )
