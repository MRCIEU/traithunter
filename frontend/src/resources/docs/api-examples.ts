export const pingSnippet = `
import requests

# Confirm the API is up and running
api_url = "https://traithunter-api.epigraphdb.org"
assert requests.get(f"{api_url}/ping").ok
`;

export const traitMappingTutorial = `
# Trait Mapping API example

Below is an example how you use the API to achive what the web app does in a similar way.
`;

export const traitMappingSnippet = `
import requests

api_url = "https://traithunter-api.epigraphdb.org"
url = f"{api_url}/entity/vector/knn"
params = {
    "id": "ieu-b-40",
    "dictionary": "opengwas",
    "dictionary_to_query": "hpo",
    "embedding_type": "bge",
    "k": 30,
}

r = requests.get(url=url, params=params)
r.raise_for_status()
res = r.json()
`;

export const pairwiseSnippet = `
import requests

api_url = "https://traithunter-api.epigraphdb.org"
url = f"{api_url}/entity/vector/pairwise-similarity"
payload = {
    "entities": [
        {
            "entity_id": "ieu-b-40",
            "dictionary": "opengwas",
        },
        {
            "entity_id": "ieu-a-296",
            "dictionary": "opengwas",
        },
        {
            "entity_id": "ieu-a-7",
            "dictionary": "opengwas",
        },
        {
            "entity_id": "ieu-a-1102",
            "dictionary": "opengwas",
        },
    ],
    "embedding_type": "bge",
}
r = client.post(url=url, json=payload)
r.raise_for_status()
res = r.json()
`;
