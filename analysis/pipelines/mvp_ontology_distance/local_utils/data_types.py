import pandera as pa
from pandera.typing import Series


class SourceDf(pa.SchemaModel):
    EFO_ID: Series[str]
    EFO_Term: Series[str]


class CleanedDf(pa.SchemaModel):
    efo_id: Series[str]
    efo_term: Series[str]
    efo_term_clean: Series[str]


class EncodeFail(pa.SchemaModel):
    efo_id: Series[str]
    term: Series[str]


class DistanceDf(pa.SchemaModel):
    id_a: Series[str]
    id_b: Series[str]
    cosine_similarity: Series[float]
