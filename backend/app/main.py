import strawberry
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from strawberry.asgi import GraphQL

TITLE = "Phenotype mapping"

app = FastAPI(title=TITLE, docs_url="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@strawberry.type
class User:
    name: str
    age: int


@strawberry.type
class Query:
    @strawberry.field
    def user(self) -> User:
        return User(name="Foobar", age=20)


schema = strawberry.Schema(query=Query)

graphql_app = GraphQL(schema)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/ping", response_model=bool)
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


@app.get("/schema", response_class=HTMLResponse, include_in_schema=False)
async def graphql_schema(request: Request):
    return templates.TemplateResponse(
        "index.html", context={"request": request}
    )
