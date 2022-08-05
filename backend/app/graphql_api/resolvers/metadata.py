from ..definitions.metadata import Metadata


def get_metadata() -> Metadata:
    desc = """Phenotype mapping"""
    ontologies = ["EFO"]
    res = Metadata(description=desc, ontologies=ontologies)
    return res
