INDEX_NAMES = {
    "hpo-bge": "hpo-2024-08-bge",
    "hpo-llama3": "hpo-2024-08-llama3",
    "ukbiobank-bge": "ukbiobank-2024-08-bge",
    "ukbiobank-llama3": "ukbiobank-2024-08-llama3",
    "icd10-bge": "icd10-2024-08-bge",
    "icd10-llama3": "icd10-2024-08-llama3",
    "opengwas-bge": "opengwas-2024-08-bge",
    "opengwas-llama3": "opengwas-2024-08-llama3",
}


DICTIONARY_NAMES = [
    "hpo", "ukbiobank", "icd10", "opengwas"
]

DICTIONARY_INDICES = {
    "hpo": "hpo-2024-08-bge",
    "ukbiobank": "ukbiobank-2024-08-bge",
    "icd10": "icd10-2024-08-bge",
    "opengwas": "opengwas-2024-08-bge",
}

INDICES = {
    "hpo": {
        "bge": "hpo-2024-08-bge",
        "llama3": "hpo-2024-08-llama3",
    },
    "ukbiobank": {
        "bge": "ukbiobank-2024-08-bge",
        "llama3": "ukbiobank-2024-08-llama3",
    },
    "icd10": {
        "bge": "icd10-2024-08-bge",
        "llama3": "icd10-2024-08-llama3",
    },
    "opengwas": {
        "bge": "opengwas-2024-08-bge",
        "llama3": "opengwas-2024-08-llama3",
    },
}

ENTITY_BASIC_FIELDS = {
    "hpo": ["id", "hpo_id", "label", "description", "type"],
    "ukbiobank": ["id", "label", "description"],
    "icd10": ["id", "label"],
    "opengwas": ["id", "label"],
}
