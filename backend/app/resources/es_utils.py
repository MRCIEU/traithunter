from app.resources import es_config


def get_entity_query(id, dictionary):
    query = {
        "query": {
            "term": {
                "id": id
            }
        },
        "_source": es_config.ENTITY_BASIC_FIELDS[dictionary]
    }
    return query


def get_entity_search(q, dictionary):
    if dictionary not in ["hpo"]:
        query = {
            "query": {
                "match": {
                    "label": q
                }
            },
            "_source": es_config.ENTITY_BASIC_FIELDS[dictionary]
        }
    else:
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"label": "body"}}
                    ],
                    "filter": [
                        {"term": {"type": "main_item"}}
                    ]
                }
            },
            "_source": es_config.ENTITY_BASIC_FIELDS[dictionary]
        }
    return query
