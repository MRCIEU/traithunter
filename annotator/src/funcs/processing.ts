import _ from "lodash";

import store from "@/store/index";
import * as types from "@/types/types";

export async function transformInputData(
  inputData: types.InputData,
): Promise<types.AnnotationData> {
  const annotationData = _.chain(inputData)
    .map((item) => {
      const selection = _.chain(
        item["equivalence_res"].concat(item["composite_res"]),
      )
        .uniqBy("ent_id")
        .value();
      const res = {
        ...item,
        selection: selection,
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
