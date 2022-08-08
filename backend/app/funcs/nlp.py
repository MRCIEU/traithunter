from functools import lru_cache
from typing import List

import numpy as np
import spacy
from loguru import logger

from app.settings import SCISPACY_LG_PATH

import scispacy  # noqa


@lru_cache()
def get_scispacy_lg() -> spacy.language.Language:
    assert SCISPACY_LG_PATH.exists(), SCISPACY_LG_PATH
    model: spacy.language.Language = spacy.load(SCISPACY_LG_PATH)
    return model


def scispacy_encode(
    text: str, nlp_model: spacy.language.Language
) -> List[float]:
    doc = nlp_model(text)
    vector = doc.vector.tolist()
    if len(vector) == 0:
        logger.info(f"empty len vector for term {text}")
    empty_vector = np.equal(np.sum(vector), 0)
    if empty_vector:
        logger.info(f"zero vector for term {text}")
        return []
    return vector
