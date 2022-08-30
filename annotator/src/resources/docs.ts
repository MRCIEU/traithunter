export const gettingStarted = `
To initialize the annotation settion,
first specify the input file and its filetype,
then specify the output file to save.

For detailed documentation please consult the
<a href="/docs" target="_blank">Documentation</a>
page.

Remember to save your progress regularly.
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

export const btnSave = "Save your progress";
export const btnExport = "Export a flat JSON file from the annotation data";

export const docsAbout = `
## Annotator for phenotype harmonization

This is a companion app for annotating phenotype mapping / harmonization results produced by the \`phenotype mapper\`.
`;

export const docsBasicUsage = ``;

export const docsFileFormat = `

\`\`\`
AnnotationDataItem = {
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
  flags: Array<FlagItem>;
  notes: string;
}
\`\`\`

`;

export const MappingStrategies = ``;
