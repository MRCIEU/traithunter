type HeaderItem = {
  text: string;
  value: string;
  align?: string;
  sortable?: boolean;
};

export const headers: Array<HeaderItem> = [
  {
    text: "Name",
    align: "start",
    value: "name",
  },
  { text: "Description", value: "desc" },
];

export const initItems = [
  {
    name: "good",
    desc: "Results for this item are good",
  },
  {
    name: "poor",
    desc: "Results for this item are very poor",
  },
  {
    name: "review",
    desc: "Require further review for the results to make a decision",
  },
  {
    name: "unmappable",
    desc: "This item is not mappable in its current state (i.e. need to use an alternative query term)",
  },
];
