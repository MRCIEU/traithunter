from typing import Any, Dict

ENTITY_ENCODES_CONFIG = {
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
                "substring": {
                    "type": "shingle",
                    "min_shingle_size": 2,
                    "max_shingle_size": 4,
                    "output_unigrams": True,
                },
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
            "vector": {
                "type": "dense_vector",
                "dims": 200,
                "index": True,
                "similarity": "cosine",
            },
        }
    },
}


def make_es_index_conf() -> Dict[str, Any]:
    return ENTITY_ENCODES_CONFIG
