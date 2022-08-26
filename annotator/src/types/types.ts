export type BaseEnt = {
  ent_id: string;
  ent_term: string;
};

export type VectorEntItem = {
  ent_id: string;
  ent_term: string;
  primary_term: boolean;
  vector_term: string;
};

export type InputDataItem = {
  trait_id: string;
  trait_term: string;
  trait_term_query: Array<string>;
  phenotype: string;
  trait_type: string;
  dataset: string;
  equivalence_res: Array<VectorEntItem>;
  equivalence_filter_res: Array<VectorEntItem>;
  composite_res: Array<VectorEntItem>;
};

export type AnnotationDataItem = {
  trait_id: string;
  trait_term: string;
  trait_term_query: Array<string>;
  phenotype: string;
  trait_type: string;
  dataset: string;
  equivalence_res: Array<VectorEntItem>;
  equivalence_filter_res: Array<VectorEntItem>;
  composite_res: Array<VectorEntItem>;
  candidates: Array<VectorEntItem>;
  selection: Array<string>;
  notes: string;
};

export type InputData = Array<InputDataItem>;
export type AnnotationDataExport = Array<AnnotationDataItem>;

export interface AnnotationData {
  [trait_id: string]: AnnotationDataItem;
}

export type FlagItem = {
  name: string;
  desc: string;
};

export type AnnotationMetadata = {
  flags: Array<FlagItem>;
};
