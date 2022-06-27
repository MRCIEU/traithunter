import json

import pandas as pd
import pandera as pa
from metaflow import FlowSpec, Parameter, step
from pandera.engines.numpy_engine import Object
from pandera.typing import DataFrame, Series
from tqdm import tqdm

from funcs import paths


class EfoNodes(pa.SchemaModel):
    ent_id: Series[str]
    ent_term: Series[str]
    synonyms: Series[Object]
    description: Series[str] = pa.Field(nullable=True)


class IndexEfoFlow(FlowSpec):

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
        self.next(self.end)

    def encode_efo(self):
        # TODO
        pass

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
                for _ in tqdm(raw_data.to_dict(orient="records"))
            ]
        )
        df = df.where(pd.notnull(df), None)
        return df


if __name__ == "__main__":
    IndexEfoFlow()
