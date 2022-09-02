// # Common types
export type BaseEnt = {
  ent_id: string;
  ent_term: string;
};

export type VectorEnt = {
  ent_id: string;
  ent_term: string;
  primary_term: boolean;
  vector_term: string;
};

export type FlagItem = {
  name: string;
  desc: string;
};

// # Mapping results

export type MappingResultsInputItem = {
  trait_id: string;
  trait_term: string;
  trait_term_query: Array<string>;
  phenotype: string;
  trait_type: string;
  dataset: string;
  equivalence_res: Array<VectorEnt>;
  equivalence_filter_res: Array<VectorEnt>;
  composite_res: Array<VectorEnt>;
};

export type MappingResultsInput = Array<MappingResultsInputItem>;

// Annotation results

export type AnnotationDataItem = {
  trait_id: string;
  trait_term: string;
  trait_term_query: Array<string>;
  trait_basic_info: {
    phenotype: string;
    trait_type: string;
    dataset: string;
  };
  equivalence_res: Array<VectorEnt>;
  composite_res: Array<VectorEnt>;
  candidates: Array<VectorEnt>;
  selection: Array<string>;
  external_selection: Array<BaseEnt>;
  flags: Array<string>;
  notes: string;
};

export type AnnotationDataExport = {
  metadata: AnnotationMetadata | null;
  data: AnnotationData;
};

export interface AnnotationData {
  [trait_id: string]: AnnotationDataItem;
}

export type AnnotationMetadata = {
  flags: Array<FlagItem>;
};

export type InputData = MappingResultsInput | AnnotationDataExport;

// Flattened results

export type FlatExportItem = {
  trait_id: string;
  trait_term: string;
  selection: Array<BaseEnt>;
  external_selection: Array<BaseEnt>;
  flags: Array<string>;
  notes: string;
};

export type FlatExportData = Array<FlatExportItem>;
