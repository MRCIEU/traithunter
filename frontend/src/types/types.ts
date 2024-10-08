// ---- basics ----

export type InfoEntity = {
  id: string;
  label: string;
};

export type BaseEnt = {
  ent_id: string;
  ent_term: string;
  dictionary: string;
};

export type EntWithScore = {
  ent_id: string;
  ent_term: string;
  dictionary: string;
  score: number;
};
