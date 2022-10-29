import _ from "lodash";

import store from "@/store/index";
import * as types from "@/types/types";

type TraitBasicInfoMapping = {
  phenotype: string;
  trait_type: string;
  dataset: string;
};

export async function initInput({
  inputData,
  inputType,
}: {
  inputData: types.InputData;
  inputType: string;
}): Promise<types.AnnotationDataExport> {
  let res = null;
  if (inputType == "mapping-results") {
    console.log("mapping-results");
    const annotationData = await initFromMapping(
      inputData as types.MappingResultsInput,
    );
    res = {
      metadata: null,
      data: annotationData,
    };
  } else if (inputType == "annotation-results") {
    console.log("annotation-results");
    res = await initFromAnnotation(inputData as types.AnnotationDataExport);
  }
  return res;
}

async function initFromAnnotation(
  inputData: types.AnnotationDataExport,
): Promise<types.AnnotationDataExport> {
  const data = inputData.data;
  const res = {
    metadata: inputData.metadata,
    data: data,
  };
  return res;
}

async function initFromMapping(
  inputData: types.MappingResultsInput,
): Promise<types.AnnotationData> {
  const annotationData = _.chain(inputData)
    .map((item) => {
      // NOTE: this version of the basic info is from 2022-07
      const traitBasicInfo: TraitBasicInfoMapping = {
        phenotype: item.phenotype,
        trait_type: item.trait_type,
        dataset: item.dataset,
      };
      const convertedItem = {
        trait_id: item.trait_id,
        trait_term: item.trait_term,
        trait_term_query: item.trait_term_query,
        trait_basic_info: traitBasicInfo,
        equivalence_res: item.equivalence_res,
        composite_res: item.composite_res,
      };
      const candidates = _.chain(
        item["equivalence_res"].concat(item["composite_res"]),
      )
        .uniqBy("ent_id")
        .value();
      const cand_flags = _.chain(candidates)
        .map((e) => e.ent_id)
        .reduce(
          (a, b) => ({
            ...a,
            [b]: [],
          }),
          {},
        )
        .value();
      const res = {
        ...convertedItem,
        candidates: candidates,
        selection: [],
        external_selection: [],
        cand_flags: cand_flags,
        trait_flags: [],
        notes: "",
      };
      return res;
    })
    .reduce((a, b) => {
      const res = {
        ...a,
        [b["trait_id"]]: b,
      };
      return res;
    }, {})
    .value();
  return annotationData;
}
