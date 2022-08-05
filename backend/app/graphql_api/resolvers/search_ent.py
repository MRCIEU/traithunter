from typing import List

from ..definitions import search_ent as search_ent_defn


def search_ent_fn(self, query: str) -> search_ent_defn.SearchEnt:
    metadata_res = search_ent_defn.SearchEntMetadata(placeholder=None)
    search_res: List[search_ent_defn.SearchEntItem] = [
        search_ent_defn.SearchEntItem(placeholder=None)
    ]
    res = search_ent_defn.SearchEnt(metadata=metadata_res, results=search_res)
    return res
