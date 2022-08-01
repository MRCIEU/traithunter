from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import strawberry
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
