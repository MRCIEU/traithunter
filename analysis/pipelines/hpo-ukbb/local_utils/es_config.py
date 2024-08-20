index_config_hpo_bge = {
    "mappings": {
        "properties": {
            "id": {
                "type": "keyword",
            },
            "hpo_id": {
                "type": "keyword",
            },
            "label": {
                "type": "text",
            },
            "description": {
                "type": "text",
            },
            "type": {
                "type": "keyword",
            },
            "vector_title": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "cosine",
            },
            "vector_full": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "cosine",
            },
        }
    },
}

index_config_hpo_llama3 = {
    "mappings": {
        "properties": {
            "id": {
                "type": "keyword",
            },
            "hpo_id": {
                "type": "keyword",
            },
            "label": {
                "type": "text",
            },
            "description": {
                "type": "text",
            },
            "type": {
                "type": "keyword",
            },
            "vector_title": {
                "type": "dense_vector",
                "dims": 4096,
                "index": True,
                "similarity": "cosine",
            },
            "vector_full": {
                "type": "dense_vector",
                "dims": 4096,
                "index": True,
                "similarity": "cosine",
            },
        }
    },
}

index_config_ukbiobank_bge = {
    "mappings": {
        "properties": {
            "id": {
                "type": "keyword",
            },
            "label": {
                "type": "text",
            },
            "description": {
                "type": "text",
            },
            "type": {
                "type": "keyword",
            },
            "vector_title": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "cosine",
            },
            "vector_full": {
                "type": "dense_vector",
                "dims": 768,
                "index": True,
                "similarity": "cosine",
            },
        }
    },
}

index_config_ukbiobank_llama3 = {
    "mappings": {
        "properties": {
            "id": {
                "type": "keyword",
            },
            "label": {
                "type": "text",
            },
            "description": {
                "type": "text",
            },
            "vector_title": {
                "type": "dense_vector",
                "dims": 4096,
                "index": True,
                "similarity": "cosine",
            },
            "vector_full": {
                "type": "dense_vector",
                "dims": 4096,
                "index": True,
                "similarity": "cosine",
            },
        }
    },
}

INDEX_NAMES = {
    "hpo-bge": "hpo-2024-08-bge",
    "hpo-llama3": "hpo-2024-08-llama3",
    "ukbiobank-bge": "ukbiobank-2024-08-bge",
    "ukbiobank-llama3": "ukbiobank-2024-08-llama3",
}

INDEX_CONFIGS = {
    "hpo-bge": index_config_hpo_bge,
    "hpo-llama3": index_config_hpo_llama3,
    "ukbiobank-bge": index_config_ukbiobank_bge,
    "ukbiobank-llama3": index_config_ukbiobank_llama3,
}
