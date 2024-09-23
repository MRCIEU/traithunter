import re
from datetime import datetime
from pathlib import Path
from string import punctuation
from typing import Any, Dict, List

import numpy as np
import ray
import requests
import spacy
from Levenshtein import distance as levenshtein_distance
from pydash import py_
from unidecode import unidecode

from analysis_funcs import settings


def clean_phenotype_id(text: str) -> str:
    text = text.lower().strip()
    for _ in punctuation:
        text = text.replace(_, "")
    text = text.replace(" ", "-")
    return text


def clean_trait_term(term: str) -> str:
    # unidecode
    term = unidecode(term)
    # Remove certain punctuation
    puncts = [
        # This is a byproduct of unidecode-ed some weird chars
        "!+",
        # regular puncts
        "/",
        ";",
        "|",
        "_",
        "+",
        "!",
    ]
    for punct in puncts:
        term = term.replace(punct, " ")
    # Remove patterns like A123
    pat = re.compile(r"[A-Z]\d+ ")
    term = re.sub(pat, " ", term)
    # Exclude list
    exclude_list = ["NOS"]
    for _ in exclude_list:
        term = term.replace(_, " ")
    # Replace certain abbrevs
    abbrevs = {"incl.": "including ", "excl.": "excluding ", "(s ": "s "}
    for k, v in abbrevs.items():
        term = term.replace(k, v)
    # remove unncessary whitespaces
    term = " ".join(term.split())
    return term


def get_kb_ents(
    ents: List[spacy.tokens.span.Span], linker: spacy.pipeline.EntityLinker
) -> List[str]:
    "Returns the canonical_name from kb ents"
    kb_ents = py_.chain([[__ for __ in _._.kb_ents] for _ in ents]).flatten().value()
    linked_ents = [linker.kb.cui_to_entity[_[0]] for _ in kb_ents]
    kb_names = [_.canonical_name for _ in linked_ents]
    return kb_names


@ray.remote(num_cpus=1)
class ItemEncoder:
    def __init__(self, idx: int, model_path: Path):
        self.idx = f"Encoder {idx}"
        print(f"{self.idx}: Init model")
        self.nlp = spacy.load(model_path)
        print(f"{self.idx}: Model loaded")

    def encode_mvp_items(self, idx: int, item: Dict[str, Any]):
        echo_step = 200
        if idx % echo_step == 0:
            now = datetime.now()
            now_str = now.strftime("%H:%M:%S")
            print(f"{now_str} {self.idx}: # {idx}")
        term = item["trait_term_clean"]
        trait_term_encode = {"term": term, "vector": self.nlp(term).vector.tolist()}
        trait_ents_encode = [
            {"term": _, "vector": self.nlp(_).vector.tolist()} for _ in item["ents"]
        ]
        res = {
            "trait_id": item["trait_id"],
            "trait_term_encode": trait_term_encode,
            "trait_ents_encode": trait_ents_encode,
        }
        return res

    def encode_chunk(self, item_list: List[Dict]):
        print(f"{self.idx}: Start to process {len(item_list)} items")
        res = [
            self.encode_mvp_items(idx=idx, item=_) for idx, _ in enumerate(item_list)
        ]
        print(f"{self.idx}: Finish process")
        return res


def query_term_embeddings(
    term: str, vector: List[float], score_threshold=0.9
) -> List[Dict[str, Any]]:
    def _main():
        empty_vector = np.equal(np.sum(vector), 0)
        if empty_vector:
            print(f"term: {term} has empty vector")
            return []
        res = _query(term=term, vector=vector, score_threshold=score_threshold)
        return res

    def _format(item: Dict[str, Any]):
        res = item["_source"].copy()
        # res["score"] = item["_score"]
        return res

    def _query(term: str, vector: List[float], score_threshold: int):
        es_url = settings.es_url
        index_name = "efo-vectors"
        url = f"{es_url}/{index_name}/_knn_search"
        payload = {
            "knn": {
                "field": "vector",
                "query_vector": vector,
                "k": 3,
                "num_candidates": 15,
            },
            "_source": ["ent_id", "ent_term", "primary_term", "vector_term"],
        }
        r = requests.get(url, json=payload)
        try:
            r.raise_for_status()
        except Exception as e:
            print(e, r.text)
            raise
        results = [
            _format(_)
            for _ in r.json()["hits"]["hits"]
            if _["_score"] >= score_threshold
        ]
        return results

    return _main()


def query_term_fulltext(term: str) -> List[Dict[str, Any]]:
    def _main():
        res = _query(term)
        return res

    def _format(item: Dict[str, Any]):
        res = item["_source"].copy()
        # res["score"] = item["_score"]
        return res

    def _query(term: str):
        es_url = settings.es_url
        index_name = "efo-vectors"
        url = f"{es_url}/{index_name}/_search"
        payload = {
            "query": {"match": {"vector_term": {"query": term}}},
            "size": 3,
            "_source": ["ent_id", "ent_term", "primary_term", "vector_term"],
        }
        r = requests.get(url, json=payload)
        r.raise_for_status()
        results = [_format(_) for _ in r.json()["hits"]["hits"]]
        return results

    return _main()


def pick_high_confidence_cands(
    term: str, cands: List[str], limit: int = 2
) -> List[str]:
    edit_dist = [
        {"cand": _, "dist": levenshtein_distance(term.lower(), _.lower())}
        for _ in cands
    ]
    res = [_["cand"] for _ in edit_dist if _["dist"] <= limit]
    return res


def get_mapping(item):
    trait_term = item["trait_term_encode"]["term"]
    trait_term_res = {
        "term": trait_term,
        "cands_embeddings": query_term_embeddings(
            term=trait_term, vector=item["trait_term_encode"]["vector"]
        ),
        "cands_fulltext": query_term_fulltext(
            term=trait_term,
        ),
    }
    trait_ents_res = [
        {
            "term": _["term"],
            "cands_embeddings": query_term_embeddings(
                term=_["term"], vector=_["vector"]
            ),
            "cands_fulltext": query_term_fulltext(term=_["term"]),
        }
        for _ in item["trait_ents_encode"]
    ]
    # high confidence: as defined by close levenshtein distance
    hc_term = pick_high_confidence_cands(
        term=trait_term,
        cands=py_.chain(
            [_["vector_term"] for _ in trait_term_res["cands_embeddings"]]
            + [_["vector_term"] for _ in trait_term_res["cands_fulltext"]]
        )
        .uniq()
        .value(),
    )
    hc_ents_nested = [
        pick_high_confidence_cands(
            term=_["term"],
            cands=py_.chain(
                [__["vector_term"] for __ in _["cands_embeddings"]]
                + [__["vector_term"] for __ in _["cands_fulltext"]]
            )
            .uniq()
            .value(),
        )
        for _ in trait_ents_res
    ]
    hc_ents = py_.chain(hc_ents_nested).flatten().uniq().value()
    high_confidence_res = hc_term if len(hc_term) > 0 else hc_ents
    # candidates
    cands_term_full = py_.chain(
        trait_term_res["cands_embeddings"] + trait_term_res["cands_fulltext"]
    ).value()
    cands_ents_full = (
        py_.chain([_["cands_embeddings"] + _["cands_fulltext"] for _ in trait_ents_res])
        .flatten()
        .value()
    )
    cands_full = cands_term_full + cands_ents_full
    cands = (
        py_.chain(cands_full)
        .map(
            lambda e: {
                "ent_id": e["ent_id"],
                "ent_term": e["ent_term"],
                "synonyms": [],
                "matched_terms": [],
                "frequency": 0,
            }
        )
        .uniq_by(lambda e: e["ent_id"])
        .value()
    )
    cands_dict = {_["ent_id"]: _ for _ in cands}
    for _ in cands_full:
        cands_dict[_["ent_id"]]["frequency"] += 1
        cands_dict[_["ent_id"]]["synonyms"].append(_["vector_term"])
    for _ in trait_term_res["cands_embeddings"] + trait_term_res["cands_fulltext"]:
        cands_dict[_["ent_id"]]["matched_terms"].append(trait_term_res["term"])
    for _ in trait_ents_res:
        for __ in _["cands_embeddings"] + _["cands_fulltext"]:
            cands_dict[__["ent_id"]]["matched_terms"].append(_["term"])
    for k in cands_dict.keys():
        cands_dict[k]["synonyms"] = list(set(cands_dict[k]["synonyms"]))
        cands_dict[k]["matched_terms"] = list(set(cands_dict[k]["matched_terms"]))
    cands = (
        py_.chain([v for v in cands_dict.values()])
        .sort(key=lambda e: e["frequency"], reverse=True)
        .value()
    )
    # picks
    # default picks are ent_ids for high confidence terms
    default_picks = [
        _["ent_id"]
        for _ in cands
        if (_["ent_term"] in high_confidence_res)
        or (len(set(_["synonyms"]).intersection(set(high_confidence_res))) > 0)
    ]
    _ent_ids_for_trait_term = (
        py_.chain([_["ent_id"] for _ in cands_ents_full]).uniq().value()
    )
    TOP_N = 15
    cands_subset = (
        py_.chain(
            (
                # results for high confidence
                [_ for _ in cands if _["ent_id"] in default_picks]
                +
                # results for the whole trait term
                [_ for _ in cands if _["ent_id"] in _ent_ids_for_trait_term]
                +
                # results sorted by frequency
                cands
            )
        )
        .uniq_by(lambda e: e["ent_id"])
        .value()[:TOP_N]
    )
    res = {
        "trait_id": item["trait_id"],
        "trait_term_mapping": trait_term_res,
        "trait_ents_mapping": trait_ents_res,
        "high_confidence_terms": high_confidence_res,
        "candidates_full": cands,
        "candidates_subset": cands_subset,
        "default_picks": default_picks,
    }
    return res


@ray.remote(num_cpus=1)
def get_mapping_remote(idx, total, item):
    echo_step = 200
    if idx % echo_step == 0:
        now = datetime.now()
        now_str = now.strftime("%H:%M:%S")
        print(f"{now_str} #{idx} / {total}")
    return get_mapping(item)
