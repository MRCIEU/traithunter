from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import dictionary, entity, utils, vector

TITLE = "TraitHunter"

app = FastAPI(title=TITLE, docs_url="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(utils.router, tags=["utils"])
app.include_router(entity.router, tags=["entity"])
app.include_router(vector.router, tags=["entity"])
app.include_router(dictionary.router, tags=["entity"])
