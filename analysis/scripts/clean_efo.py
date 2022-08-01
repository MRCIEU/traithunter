import json

import pandas as pd
import pandera as pa
import spacy
from metaflow import FlowSpec, Parameter, step
from pandera.engines.numpy_engine import Object
from pandera.typing import DataFrame, Series

from analysis_funcs import paths
from analysis_funcs.embeddings import scispacy_encode

import scispacy  # noqa

LOGGER_STEP = 200


class EfoNodes(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    synonyms: Series[Object]
    description: Series[str] = pa.Field(nullable=True)


class EfoEncodes(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    vector_term: Series[str]
    vector: Series[Object]
    primary_term: Series[bool]


class CleanEfoFlow(FlowSpec):

    OVERWRITE = Parameter(
        "overwrite",
        help="overwrite",
        default=False,
        is_flag=True,
    )

    @step
    def start(self):
        self.efo_raw_path = paths.data["efo"]
        assert self.efo_raw_path.exists(), self.efo_raw_path
        with self.efo_raw_path.open() as f:
            efo_raw = json.load(f)
        self.efo = efo_raw["graphs"][0]
        self.next(self.prep_efo_data)

    @step
    def prep_efo_data(self):
        self.efo_ents_path = paths.data["artifacts"] / "cleaned_efo_ents.json"
        if not self.efo_ents_path.exists() or self.OVERWRITE:
            efo_nodes = pd.json_normalize(self.efo["nodes"])
            efo_ents = self._prep_efo_ents(efo_nodes)
            with self.efo_ents_path.open("w") as f:
                json.dump(efo_ents.to_dict(orient="records"), f)
        else:
            with self.efo_ents_path.open() as f:
                efo_ents = pd.json_normalize(json.load(f))
        self.efo_ents = efo_ents
        self.next(self.encode_efo)

    @step
    def encode_efo(self):
        self.efo_encode_path = paths.data["artifacts"] / "encoded_efo_ents.json"
        if not self.efo_encode_path.exists() or self.OVERWRITE:
            efo_encode = self._encode_efo(self.efo_ents)
            with self.efo_encode_path.open("w") as f:
                json.dump(efo_encode.to_dict(orient="records"), f)
        else:
            with self.efo_encode_path.open() as f:
                efo_encode = pd.json_normalize(json.load(f))
        self.efo_encode = efo_encode
        self.next(self.end)

    @step
    def end(self):
        pass

    @pa.check_types
    def _prep_efo_ents(self, raw_data: pd.DataFrame) -> DataFrame[EfoNodes]:
        def _get_synonyms(item):
            res = []
            if not isinstance(item, list):
                return res
            res = [_["val"] for _ in item if _["pred"] == "hasExactSynonym"]
            return res

        # type "PROPERY" is for edge type of nodes
        # only "CLASS" is valid
        raw_data = raw_data[raw_data["type"].isin(["CLASS"])]
        raw_data = raw_data.dropna(subset=["id", "lbl"])
        raw_data = raw_data.reset_index(drop=True)
        df = pd.DataFrame(
            [
                {
                    "ent_id": _["id"],
                    "ent_term": _["lbl"],
                    "description": _["meta.definition.val"],
                    "synonyms": _get_synonyms(_["meta.synonyms"]),
                }
                for _ in raw_data.to_dict(orient="records")
            ]
        )
        df = df.where(pd.notnull(df), None)
        return df

    @pa.check_types
    def _encode_efo(self, efo_ents: DataFrame[EfoNodes]) -> DataFrame[EfoEncodes]:
        print("Init model")
        model_path = paths.models["scispacy_lg"]
        nlp_model: spacy.language.Language = spacy.load(model_path)
        print("Perform encoding")
        res = []
        total = len(efo_ents)
        for idx, row in efo_ents.iterrows():
            if idx % LOGGER_STEP == 0:
                print(f"# {idx} / {total}")
            primary_item = {
                "ent_id": row["ent_id"],
                "ent_term": row["ent_term"],
                "primary_term": True,
                "vector_term": row["ent_term"],
                "vector": scispacy_encode(row["ent_term"], nlp_model=nlp_model),
            }
            res.append(primary_item)
            if len(row["synonyms"]) > 0:
                for item in row["synonyms"]:
                    synonym_item = {
                        "ent_id": row["ent_id"],
                        "ent_term": row["ent_term"],
                        "primary_term": False,
                        "vector_term": item,
                        "vector": scispacy_encode(item, nlp_model=nlp_model),
                    }
                    res.append(synonym_item)
        res_df = pd.DataFrame(res).drop_duplicates(subset=["ent_id", "vector_term"])
        return res_df


if __name__ == "__main__":
    CleanEfoFlow()
