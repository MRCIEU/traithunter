# MVP phenotype terms, round 2

## Overall strategies

## Data cleaning

- Datasets involved are the previous MVP phenotype terms (UKBB+MVP), and the new dataset involving Biobank Japan and FinnGenn terms
- Trait ids are fomulated as `<source>-<phenotype/phenocode>-<index>` (index is used as there are cases of different id-label cominbations)
  - Original item properties will be preserved in the `trait_basic_info` property
- ...
- The cleaned dataset will be merged with a manual annotation on term labels
  - i.e. The term labels to be mapped to ontologies will be from both cleaned labels as well as manual annotation labels
  
## Mapping

## Scratch

- abbrevs are not neccessary as all abbrevs have been companied by their full terms