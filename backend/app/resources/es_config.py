INDEX_NAMES = {
    "hpo-bge": "hpo-2024-08-bge",
    "hpo-llama3": "hpo-2024-08-llama3",
    "ukbiobank-bge": "ukbiobank-2024-08-bge",
    "ukbiobank-llama3": "ukbiobank-2024-08-llama3",
    "icd10-bge": "icd10-2024-08-bge",
    "icd10-llama3": "icd10-2024-08-llama3",
}


DICTIONARY_NAMES = [
    "hpo", "ukbiobank", "icd10"
]

DICTIONARY_INDICES = {
    "hpo": "hpo-2024-08-bge",
    "ukbiobank": "ukbiobank-2024-08-bge",
    "icd10": "icd10-2024-08-bge",
}

ENTITY_BASIC_FIELDS = {
    "hpo": ["id", "hpo_id", "label", "description", "type"],
    "ukbiobank": ["id", "label", "description"],
    "icd10": ["id", "label"],
}
