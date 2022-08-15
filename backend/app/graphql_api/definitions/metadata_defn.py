from typing import List

import strawberry

_docs = "Metadata information"


@strawberry.type(description=_docs)
class Metadata:
    description: str
    ontologies: List[str]


def resolver() -> Metadata:
    desc = """Phenotype mapping"""
    ontologies = ["EFO"]
    res = Metadata(description=desc, ontologies=ontologies)
    return res
