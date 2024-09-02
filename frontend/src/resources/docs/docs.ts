export const hello = `Hello`;

export const topDoc = `
TraitHunter is a platform to search and map biomedical traits across
various major dictionaries.

The dictionaries we curate and offer search functionalities include:

- OpenGWAS traits (2024-08)
- ICD10 codes (2024-08)
- HPO ontology terms (2024-08)
- UKBiobank variables (2024-08)
`;

export const aboutDesc = `
This platform curates various biomedical dictionaries (e.g. ontologies).

This web platform (and its API) provides the following functionalities:

- Mapping of traits via semantic similarties
- Pairwise semantic similarity of traits
`;

export const traitMappingDoc = `
Search and map a trait to trait in other dictionaries
via the text embeddings of its label (k-Nearest Neighbour search).

## How to use

1. Select a source trait entity of interest
    1. Select the dictionary of the source entity
    1. Search for the source entity of interest by its label
1. Select the dictionary of the target entities
1. Configure other variables
1. Click on the submit button
`;

export const pairwiseDoc = `
Compute the pairwise cosine similarity scores
for the inluded list of trait entities,
via the text embeddings of their labels.
`;

export const dataExplorerDoc = `
Data explorer for entities in a dictionary.

NOTE: this is just a preview pilot and is subject to change.
`;
