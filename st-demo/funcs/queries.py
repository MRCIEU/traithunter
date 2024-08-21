import requests

API_URL = "http://backend"

def ping():
    r = requests.get(f"{API_URL}/ping", params={"dependencies": False})
    return r.json()

def search_entity(q, dictionary):
    url = f"{API_URL}/entity/search"
    params = {
        "q": q,
        "dictionary": dictionary
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

def knn(id, dictionary, dictionary_to_query, embedding_type):
    url = f"{API_URL}/entity/knn"
    params = {
        "id": id,
        "dictionary": dictionary,
        "dictionary_to_query": dictionary_to_query,
        "embedding_type": embedding_type,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()
