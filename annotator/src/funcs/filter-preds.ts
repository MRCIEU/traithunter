import _ from "lodash";

import * as types from "@/types/types";

function emptyPicks(e: types.AnnotationDataItem): boolean {
  const res = e.selection.length == 0;
  return res;
}

function nonEmptyPicks(e: types.AnnotationDataItem): boolean {
  const res = e.selection.length > 0;
  return res;
}

function hasExternalPicks(e: types.AnnotationDataItem): boolean {
  const res = e.external_selection.length > 0;
  return res;
}

function hasNotes(e: types.AnnotationDataItem): boolean {
  const res = e.notes.length > 0;
  return res;
}

export const preds = [
  {
    name: "empty-picks",
    label: "Items WITHOUT picks from candidates",
    func: emptyPicks,
  },
  {
    name: "non-empty-picks",
    label: "Items with picks from candidates",
    func: nonEmptyPicks,
  },
  {
    name: "has-external-picks",
    label: "Items with external picks",
    func: hasExternalPicks,
  },
  {
    name: "has-notes",
    label: "Items that contain notes",
    func: hasNotes,
  },
];
