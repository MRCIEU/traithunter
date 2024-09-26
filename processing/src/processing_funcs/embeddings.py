from typing import List

import spacy
from loguru import logger


def scispacy_encode(text: str, nlp_model: spacy.language.Language) -> List[float]:
    doc = nlp_model(text)
    vector = doc.vector.tolist()
    if len(vector) == 0:
        logger.info(f"empty vector for term {text}")
    return vector
