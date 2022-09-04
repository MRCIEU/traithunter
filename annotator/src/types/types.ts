// # Overview
//
// - The 2022-07 mapping results format is declared by `MappingResultsInput`,
//   which is an array (list) of individual `MappingResultsInputItem`.
// - The 2022-09 annotation results format is declared by `AnnotationDataExport`,
//   which is an object (dictionary) with a metadata field, and a data field.
//   The data field is declared by `AnnotationData`.
// - The flattened results format, `FlatExportData`, is an array of simplified
//   annotation data item.
// - For a concept entity, its basic form is `BaseEnt`, and the vectorized form
//   is `VectorEnt`.
//   An entity retrieved from the vector store is `VectorEnt`, where either its
//   primary term or one of its synonym is used to generate the embedding vector.
//   `BaseEnt` is used in situations such as adding
//   external concept (ontology) entities.

// # Common types

export type BaseEnt = {
  // `BaseEnt` is the basic building block of a "concept entity",
  // which must have an identifier and a term label
  ent_id: string;
  ent_term: string;
};

export type VectorEnt = {
  // `VectorEnt` is a concept entity, vectorized by vector_term.
  // In other words, the primary term label (ent_term) is not necessarily
  // the label wehre the vector is generated from.
  ent_id: string;
  ent_term: string;
  // true when vector_term is the same with ent_term otherwise false.
  // When primary_term is false, it means that the vector is generated from
  // a synonym label of the concept entity, rather than the primary label.
  primary_term: boolean;
  vector_term: string;
};

export type FlagItem = {
  // A `FlagItem` has a name field, which is a short label on the flag,
  // and a description field, which is a longer label.
  name: string;
  desc: string;
};

// # Mapping results
// NOTE: This is the 2022-07 format, which should be treated as
// legacy and will not be used in future files.

export type MappingResultsInputItem = {
  trait_id: string;
  trait_term: string;
  trait_term_query: Array<string>;
  phenotype: string;
  trait_type: string;
  dataset: string;
  // Mapping results from the equivalence mapping strategy
  equivalence_res: Array<VectorEnt>;
  // Subset of the mapping results, with greater confidence
  // NOTE: this is not in use in the annotator
  equivalence_filter_res: Array<VectorEnt>;
  // Mapping results from the composite mapping strategy
  composite_res: Array<VectorEnt>;
};

export type MappingResultsInput = Array<MappingResultsInputItem>;

// Annotation results

export type AnnotationDataItem = {
  trait_id: string;
  trait_term: string;
  trait_term_query: Array<string>;
  trait_basic_info: {
    // Data availability inside `trait_basic_info` is subjected to
    // the source data
    phenotype: string;
    trait_type: string;
    dataset: string;
  };
  // Mapping results from equivalence mapping strategy
  equivalence_res: Array<VectorEnt>;
  // Mapping results from composite mapping strategy
  composite_res: Array<VectorEnt>;
  // Concept entities aggregated from
  // both `equivalence_res` and `composite_res`
  candidates: Array<VectorEnt>;
  // Array of `ent_id` of `candidates`
  selection: Array<string>;
  // Picks from external source, if the candidates from mapping results
  // are not satisfactory
  external_selection: Array<BaseEnt>;
  // Flag names
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
