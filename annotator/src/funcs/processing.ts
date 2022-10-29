import _ from "lodash";

import store from "@/store/index";
import * as types from "@/types/types";

export async function flatDataExport(
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
        trait_flags: e.trait_flags,
        notes: e.notes,
      };
      return res;
    })
    .value();
  return res;
}
