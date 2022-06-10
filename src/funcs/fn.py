import re
import json
from pathlib import Path
from typing import Any, Dict, List
from string import punctuation

import requests
import pandas as pd
import janitor
import numpy as np
from loguru import logger

def clean_text(text: str) -> str:
    # drop A123 like
    pat = re.compile("[A-Z]\d+ ")
    text = re.sub(pat, "", text)
    # drop punctuation
    for _ in punctuation:
        text = text.replace(_, " ")
    # lowercase
    text = text.lower()
    return text

def search_epigraphdb_efo(text: str, limit: int = 5) -> List[Dict[str, Any]]:
    url = "https://api.epigraphdb.org/nlp/query/text"
    params = {"text": text, "asis": True, "include_meta_nodes": ["Efo"], "limit": limit}
    r = requests.get(url, params=params)
    r.raise_for_status()
    res = [
        {
            "id": _["id"],
            "name": _["name"],
            "score": _["score"],
        }
        for _ in r.json()["results"]["results"]
    ]
    return res

