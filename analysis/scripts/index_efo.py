import json
from typing import Any, Dict, List

from loguru import logger
from metaflow import FlowSpec, Parameter, step

from funcs import es, paths, settings

LOGGER_STEP = 20
LITE_NUM = 1_000
ES_URL = settings.es_url
EFO_ENTS_CONFIG = {
    "settings": {
        "analysis": {
            "analyzer": {
                "substring": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "kstem", "substring"],
                },
                "exact": {
                    "type": "custom",
                    "tokenizer": "keyword",
                    "filter": [
                        "sufficient_char_length",
                        "lowercase",
                        "kstem",
                    ],
                },
            },
            "filter": {
                "sufficient_char_length": {
                    "type": "length",
                    "min": 4,
                },
                "substring": {"type": "shingle",
                              "min_shingle_size": 2,
                              "max_shingle_size": 4,
                              "output_unigrams": True},
            },
        }
    },
    "mappings": {
        "properties": {
            "ent_id": {
                "type": "keyword",
            },
            "ent_term": {
                "type": "text",
                "fields": {
                    "raw": {
                        "type": "text",
                        "analyzer": "exact",
                        "search_analyzer": "substring",
                    }
                },
            },
            "description": {
                "type": "text",
            },
            "synonyms": {
                "type": "text",
            },
        }
    },
}
EFO_ENCODES_CONFIG = {
    "settings": {
        "analysis": {
            "analyzer": {
                "substring": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "kstem", "substring"],
                },
                "exact": {
                    "type": "custom",
                    "tokenizer": "keyword",
                    "filter": [
                        "sufficient_char_length",
                        "lowercase",
                        "kstem",
                    ],
                },
            },
            "filter": {
                "sufficient_char_length": {
                    "type": "length",
                    "min": 4,
                },
                "substring": {"type": "shingle",
                              "min_shingle_size": 2,
                              "max_shingle_size": 4,
                              "output_unigrams": True},
            },
        }
    },
    "mappings": {
        "properties": {
            "ent_id": {
                "type": "keyword",
            },
            "ent_term": {
                "type": "text",
            },
            "vector_term": {
                "type": "text",
                "fields": {
                    "raw": {
                        "type": "text",
                        "analyzer": "exact",
                        "search_analyzer": "substring",
                    }
                },
            },
            "primary_term": {
                "type": "boolean",
            },
            "vector": {
                "type": "dense_vector",
                "dims": 200,
                "index": True,
                "similarity": "cosine",
            },
        }
    },
}


class IndexEfoFlow(FlowSpec):

    OVERWRITE = Parameter(
        "overwrite",
        help="overwrite",
        default=False,
        is_flag=True,
    )

    LITE = Parameter(
        "lite",
        help="lite",
        default=False,
        is_flag=True,
    )

    @step
    def start(self):
        self.next(self.index_efo_ents)

    @step
    def index_efo_ents(self):
        index_name = "efo-ents" if not self.LITE else "efo-ents-lite"
        if not es.index_exists(ES_URL, index_name) or self.OVERWRITE:
            efo_ents_path = paths.data["artifacts"] / "cleaned_efo_ents.json"
            assert efo_ents_path.exists(), efo_ents_path
            with efo_ents_path.open() as f:
                efo_ents = json.load(f)
                if self.LITE:
                    efo_ents = efo_ents[:LITE_NUM]
            es.drop_index(ES_URL, index_name)
            es.init_index(ES_URL, index_name, EFO_ENTS_CONFIG)
            logger.info(f"indexing {index_name}")
            self._index_efo_ents(efo_ents, index_name)
        else:
            logger.info(f"index {index_name} exists, skip")
        self.next(self.index_efo_vectors)

    @step
    def index_efo_vectors(self):
        index_name = "efo-vectors" if not self.LITE else "efo-vectors-lite"
        if not es.index_exists(ES_URL, index_name) or self.OVERWRITE:
            efo_encodes_path = paths.data["artifacts"] / "encoded_efo_ents.json"
            assert efo_encodes_path.exists(), efo_encodes_path
            with efo_encodes_path.open() as f:
                efo_encodes = json.load(f)
                if self.LITE:
                    efo_encodes = efo_encodes[:LITE_NUM]
            es.drop_index(ES_URL, index_name)
            es.init_index(ES_URL, index_name, EFO_ENCODES_CONFIG)
            logger.info(f"indexing {index_name}")
            self._index_efo_vectors(efo_encodes, index_name)
        else:
            logger.info(f"index {index_name} exists, skip")
        self.next(self.end)

    @step
    def end(self):
        pass

    def _index_efo_ents(self, efo_ents: List[Dict[str, Any]], index_name: str):
        index_data = [
            {
                "ent_id": _["ent_id"],
                "ent_term": _["ent_term"],
                "description": _["description"],
                "synonyms": _["synonyms"],
            }
            for _ in efo_ents
        ]
        es.bulk_index(
            es_url=ES_URL,
            index_name=index_name,
            docs=index_data,
            logger_step=LOGGER_STEP,
        )

    def _index_efo_vectors(self, efo_encode: List[Dict[str, Any]], index_name: str):
        index_data = efo_encode
        es.bulk_index(
            es_url=ES_URL,
            index_name=index_name,
            docs=index_data,
            logger_step=LOGGER_STEP,
        )


if __name__ == "__main__":
    IndexEfoFlow()
