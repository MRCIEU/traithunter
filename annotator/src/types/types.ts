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

export type MappingResultsInputItem = {
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
  trait_basic_info: {
    phenotype: string;
    trait_type: string;
    dataset: string;
  };
  equivalence_res: Array<VectorEntItem>;
  composite_res: Array<VectorEntItem>;
  candidates: Array<VectorEntItem>;
  selection: Array<string>;
  external_selection: Array<BaseEnt>;
  flags: Array<string>;
  notes: string;
};

export type MappingResultsInput = Array<MappingResultsInputItem>;

export type AnnotationDataExport = {
  metadata: AnnotationMetadata | null;
  data: AnnotationData;
};

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

export type InputData = MappingResultsInput | AnnotationDataExport;

export type FlatExportItem = {
  trait_id: string;
  trait_term: string;
  selection: Array<BaseEnt>;
  external_selection: Array<BaseEnt>;
  flags: Array<string>;
  notes: string;
};
export type FlatExportData = Array<FlatExportItem>;
