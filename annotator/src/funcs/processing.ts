import _ from "lodash";

import store from "@/store/index";
import * as types from "@/types/types";

export async function transformInputData({
  inputData,
  inputType,
}: {
  inputData: types.InputData;
  inputType: string;
}): Promise<types.AnnotationDataExport> {
  let res = null;
  if (inputType == "mapping-results") {
    console.log("mapping-results");
    const annotationData = await transformInputDataFromMappingResults(
      inputData as types.MappingResultsInput,
    );
    res = {
      metadata: null,
      data: annotationData,
    };
  } else if (inputType == "annotation-results") {
    console.log("annotation-results");
    res = await transformInputDataFromAnnotationResults(
      inputData as types.AnnotationDataExport,
    );
  }
  return res;
}

export async function transformInputDataFromAnnotationResults(
  inputData: types.AnnotationDataExport,
): Promise<types.AnnotationDataExport> {
  const res = {
    metadata: inputData.metadata,
    data: inputData.data,
  };
  return res;
}

export async function transformInputDataFromMappingResults(
  inputData: types.MappingResultsInput,
): Promise<types.AnnotationData> {
  const annotationData = _.chain(inputData)
    .map((item) => {
      const convertedItem = {
        trait_id: item.trait_id,
        trait_term: item.trait_term,
        trait_term_query: item.trait_term_query,
        trait_basic_info: {
          phenotype: item.phenotype,
          trait_type: item.trait_type,
          dataset: item.dataset,
        },
        equivalence_res: item.equivalence_res,
        composite_res: item.composite_res,
      };
      const candidates = _.chain(
        item["equivalence_res"].concat(item["composite_res"]),
      )
        .uniqBy("ent_id")
        .value();
      const res = {
        ...convertedItem,
        candidates: candidates,
        selection: [],
        external_selection: [],
        flags: [],
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

export async function transformFlatExportData(
  annotationData: types.AnnotationData,
): Promise<types.FlatExportData> {
  const res = _.chain(annotationData)
    .values()
    .map((e) => {
      const selection = _.chain(e.candidates)
        .filter((cand) => e.selection.includes(cand.ent_id))
        .map((cand) => ({ ent_id: cand.ent_id, ent_term: cand.ent_term }))
        .value();
      const res = {
        trait_id: e.trait_id,
        trait_term: e.trait_term,
        selection: selection,
        external_selection: e.external_selection,
        flags: e.flags,
        notes: e.notes,
      };
      return res;
    })
    .value();
  return res;
}
