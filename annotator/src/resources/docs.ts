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

This is a companion app for annotating phenotype mapping / harmonization results produced by the \`phenotype mapper\` (the main app is unreleased yet).
`;

export const docsGettingStarted = `
This section covers the basic steps of using this app.

For detailed documentation please consult the
<a href="/docs" target="_blank">Documentation</a>
page.

- First select the input dataset from your local filesystem, then specify the type of the input data.
For input types,
if your initial dataset is the 2022-07 mapping results data, then select "Mapping results",
and if your initial dataset is a 2022-09 annotation results data (e.g. saved from an earlier session),
then select "Annotation results".
- Then select the location in the local filesystem to save the annotation results to.
- You can now begin (or resume) the work on the annotation. Remember to save the progress regularly.
- If you need a flattened output dataset (e.g. to be consumed in a downstream analysis), you can choose the "Export flat file" option. You could also use the full annotation results directly, since the flattend results is a simplified snapshot of the full results.
`;

export const docsTechSpecs = `
## Overview

The fundamental strategy we take in terms of harmonizing biomedical concept, e.g. harmonizing between GWAS traits and ontology terms, is to employ a set of NLP techniques (primarily using vectorized harmonization) to recommend a list of candidates for a reviewer to manually review and annotate.
Therefore the annotator app is developed for the second stage of the workflow.

In terms of mapping a query term with concepts, we first apply a set of preprocessing rules to the query term, then encode the processed query term into a high-dimensional vector, and a similar process is applied to the concepts curated from the various sources.
In this way we compare the vectorized form of the query with the vectorized form of the curated concepts and return the most similar ones based on the cosine similarities of the comparing vectors.

For a biomedical concept from an ontology (e.g. Experimental Factor Ontology; EFO) it will have an **identifier** (ID/URI), a **primary term** label, and a set of **synonyms**.
We encode each of the synonyms into vectors separately, so a matching result can be due to the query term is being mapped to the primary term label, or one of the synonyms.
Therefore in \`VectorEnt\` the field \`vector_term\` from which the encoding vector is generated can come from the primary term (\`primary_term == true\`) or from a synonym (\`primary_term == false\`).

## Mapping strategies

We perform two mapping strategies to map the query term to candidates:
- A **equivalence mapping** strategy where the retrieved results are considered as to be equivalent
  to the query term (specifically one of its processed query term in \`trait_term_query\`).
- A **composite mapping** strategy where the query term is first broken into several semantic component, then for each of the component an *equivalence mapping* is attempted to retrieve its equivalent concept.
  This is useful when the original query term is a complex term describing multiple concepts or phenomena.

As a manual review is expected (with the assistance of the annotator app), we will retrive a list of results with high confidence but with a degree of tolerance for false positives, and leave the decision on which candidate to pick to the user according to the specific needs of the downstream use.

Further documentation (such as parameters on the retrieval of results) will be available in due course when the development matures further.
`;

export const docsTypes = `
You will find below the about how major objects (e.g. structure for an output file) are
defined / declared, in typescript typing syntax.
`;

export const docsChangelog = `
## Changelog

**Dev**

- Introduced flags for mapping candidates
- Flags for query traits are now called \`trait_flags\` to distinguish from \`cand_flags\` (flags for mapping candidates)

**2022-09-12, version 0.1.0**

This is the pilot release of the annotator app.
`;
