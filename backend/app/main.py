from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

TITLE = "Phenotype mapping"

app = FastAPI(title=TITLE, docs_url="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
