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
`;

export const docsTypes = `
You will find below the about how major objects (e.g. structure for an output file) are
defined / declared, in typescript typing syntax.
`;
