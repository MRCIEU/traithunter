export const gettingStarted = `
To initialize the annotation settion,
first specify the input file and its filetype,
then specify the output file to save.

For detailed documentation please consult the
<a href="/docs" target="_blank">Documentation</a>
page.

This is currently a very **alpha-stage** software.
Please keep regular backups, and remember to save your progress regularly.
`;

export const inputConfig = `
# Input configuration

- **input file**: Read in the file from local file system
- **file type**:
  - *Mapping results*: The 2022-07 mapping results format
    (typical filename is "results_general.json").
  - *Annotation results*: The 2022-09 annotation results format,
    which is also the file format you save the annotation results in.
    You should use this if you are loading from an earlier save file.
`;

export const outputConfig = `
# Output configuration

- **output file**:
  Specify the location in the filesystem to save the annotation results to.
  **NOTE**: *if you save the file to an existing location it will REPLACE the existing file*.
`;

export const btnSave = "Save your progress";
export const btnExport = `
Export a simplified and flattened JSON file from the annotation data that is easier to be imported for further analysis

**NOTE**: the flat file is a simplified snapshot of the main annotation results file, and therefore not its substitute.
`;

export const docsAbout = `
## Annotator for phenotype harmonization

This is a companion app for annotating phenotype mapping / harmonization results produced by the \`phenotype mapper\`.
`;

export const docsBasicUsage = ``;

export const docsTechSpecs = `
## Overview

TODO: overview desc

TODO: Vector entity

TODO: annotation results and flattened results

## Mapping strategies

## File format and object structure

Below are specifications of the file format in the syntax of typescript types.

### Structure of the mapping results

### Structure of the annotation results format

\`\`\`
type AnnotationDataExport = {                 # The annotation results file contains a metadata field and a data field
  metadata: AnnotationMetadata
  data: AnnotationData;
};

type AnnotationData {                         # AnnotationData is an object (dictionary) where for one item the key is a \`trait_id\` and the value is a \`AnnotationDataItem\` (see below)
  [trait_id: string]: AnnotationDataItem;
}

type AnnotationDataItem = {                   # This is the structure of the individual query item
  trait_id: string;                           # Identifier of the trait
  trait_term: string;                         # Term label of the trait
  trait_term_query: Array<string>;            # A list of actual term queries of the trait
  trait_basic_info: {                         # Other basic information regarding the trait, nested into one field.
    phenotype: string;                        #
    trait_type: string;                       #
    dataset: string;                          #
  };                                          #
  equivalence_res: Array<VectorEnt>;          # Mapping results from equivalence mapping strategy
  composite_res: Array<VectorEnt>;            # Mapping results from composite mapping strategy
  candidates: Array<VectorEnt>;               # Candidates merged from \`equivalence_res\` and \`composite_res\`
  selection: Array<string>;                   # Selected candidates in the form of \`trait_id\` strings
  external_selection: Array<BaseEnt>;         # Manually added candidates from external sources if results from \`candidates\` are not satisfactory
  flags: Array<string>;                       # Flags on this query item
  notes: string;                              # Notes on this query item
}

type AnnotationMetadata = {                   # This is the metadata field for the annotation results
  flags: Array<FlagItem>;                     # Flags where each has a name field a a description field
};
\`\`\`

### Structure of the flattened results

type FlatExportData = Array<FlatExportItem>;  #

type FlatExportItem = {                       #
  trait_id: string;                           #
  trait_term: string;                         #
  selection: Array<BaseEnt>;                  #
  external_selection: Array<BaseEnt>;         #
  flags: Array<string>;                       #
  notes: string;                              #
};

### Common object format

\`\`\`
type BaseEnt = {                              # This is the basic building block of an "entity" which must have an identifier and a label
  ent_id: string;
  ent_term: string;
};

type VectorEnt = {                            # A vector entity is the entity in the vector store
  ent_id: string;                             #
  ent_term: string;                           #
  vector_term: string;                        # This is the term label of the embeded vector
  primary_term: boolean;                      # Whether the \`vector_term\` is the embedded term
};
\`\`\`

`;

export const MappingStrategies = `
TODO
`;
