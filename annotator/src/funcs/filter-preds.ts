import _ from "lodash";

import * as types from "@/types/types";

function emptyPicks(e: types.AnnotationDataItem): boolean {
  const internalEmpty = e.selection.length == 0;
  const externalEmpty = e.external_selection.length == 0;
  const res = internalEmpty && externalEmpty;
  return res;
}

function nonEmptyPicks(e: types.AnnotationDataItem): boolean {
  const internalPicked = e.selection.length > 0;
  const externalPicked = e.external_selection.length > 0;
  const res = internalPicked || externalPicked;
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
    label: "Items WITHOUT picks (internal AND external) from candidates",
    func: emptyPicks,
  },
  {
    name: "non-empty-picks",
    label: "Items with picks (internal OR external) from candidates",
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
