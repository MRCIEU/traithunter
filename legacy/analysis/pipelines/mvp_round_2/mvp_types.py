import pandera as pa
from pandera.engines.numpy_engine import Object
from pandera.typing import Series


class CleanedDf(pa.SchemaModel):
    "The df out of the data cleaning notebook"
    trait_id: Series[str]
    trait_term: Series[str]
    trait_term_clean: Series[str]
    trait_basic_info: Series[Object]
