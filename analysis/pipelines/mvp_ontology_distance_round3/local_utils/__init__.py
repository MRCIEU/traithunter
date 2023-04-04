def get_es_index_for_source(source: str, trial: bool) -> str:
    trial_str = "--trial" if trial else ""
    res = "mvp-ontology-source-{source}{trial_str}".format(
        source=source.lower(), trial_str=trial_str
    )
    return res
