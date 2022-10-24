<template lang="pug">
v-container(fluid)
  div(v-if="dataItemsSimple != null")
    h2 Filters
    v-row
      v-col(cols="6")
        h3 Predefined filters
        v-subheader Will show items that satisfy ALL of the predicates
        div(style="overflow-y: scroll; max-height: 500px")
          v-checkbox(
            v-for="(item, idx) in preds",
            :key="idx",
            :label="item.label",
            :value="item.name",
            v-model="predSelect"
          )
      v-col(cols="6")
        h3 Flag filter for query items
        v-subheader When enabled, will show query items that contain ANY of the included flags (they first need to exist in the metadata settings)
        v-checkbox(label="Enable query item flag filter", v-model="useQueryFlagFilter")
        v-combobox(
          v-model="queryFlagSelect",
          :items="flagItems",
          chips,
          clearable,
          label="flags",
          multiple,
          preprend-icon="mdi-filter-variant",
        )
          template(v-slot:selection="{ attrs, item, select, selected }")
            v-chip(
              v-bind="attrs",
              :input-value="selected",
              close,
              @click="select",
              @click:close="queryFlagRemove(item)"
            )
              span {{ item }} &nbsp;
        h3 Flag filter for mapping candidate items
        v-subheader When enabled, will show query items that contain ANY of the included flags for the mapping candidates (they first need to exist in the metadata settings)
        v-checkbox(label="Enable candidate flag filter", v-model="useCandFlagFilter")
        v-combobox(
          v-model="candFlagSelect",
          :items="flagItems",
          chips,
          clearable,
          label="flags",
          multiple,
          preprend-icon="mdi-filter-variant",
        )
          template(v-slot:selection="{ attrs, item, select, selected }")
            v-chip(
              v-bind="attrs",
              :input-value="selected",
              close,
              @click="select",
              @click:close="candFlagRemove(item)"
            )
              span {{ item }} &nbsp;
    v-btn(color="primary", x-large, @click="updateFilter") Update filter
    .py-2
      span Current number of items: {{ dataItemsSimple.length }}
    h2 Results table
    v-data-iterator(
      :items="dataItemsSimple",
      item-key="trait_id",
      :items-per-page="5",
      :search="search"
    )
      template(v-slot:header)
        v-toolbar.mb-1(dark, color="teal lighten-1")
          v-row
            v-spacer
            v-col(cols="8")
              v-text-field(
                v-model="search",
                clearable,
                flat,
                solo-inverted,
                hide-details,
                label="Search query term"
              )
            v-spacer
      template(v-slot:default="props")
        div(v-for="item in props.items", :key="item.trait_id")
          item-display(
            :idx="item.idx",
            :trait-id="item.trait_id",
            :trait-term="item.trait_term"
          )
          v-divider
          .py-2
</template>

<script lang="ts">
import Vue from "vue";
import ItemDisplay from "@/components/widgets/ItemDisplay.vue";
import * as types from "@/types/types";
import { preds } from "@/funcs/filter-preds";

type DataItemsSimple = Array<{
  idx: number;
  trait_id: string;
  trait_term: string;
}>;

export default Vue.extend({
  name: "DataTable",
  components: {
    ItemDisplay,
  },
  data() {
    return {
      search: null,
      preds: preds,
      dataItems: [],
      predSelect: [],
      useQueryFlagFilter: false,
      useCandFlagFilter: false,
      queryFlagSelect: [],
      candFlagSelect: [],
    };
  },
  computed: {
    dataItemsSimple(): DataItemsSimple {
      const dataItems = this.dataItems;
      const res = this._.chain(dataItems)
        .map((e) => ({ trait_id: e.trait_id, trait_term: e.trait_term }))
        .map((e, idx) => ({ idx: idx, ...e }))
        .value();
      return res;
    },
    predFuncs() {
      const res = this._.chain(this.preds)
        .filter((e) => this.predSelect.includes(e.name))
        .map((e) => e.func)
        .value();
      return res;
    },
    flagItems(): Array<string> {
      const flags = this.$store.state.annotationData.metadata.flags;
      const res = this._.chain(flags)
        .map((e) => e.name)
        .value() as Array<string>;
      return res;
    },
  },
  async mounted() {
    this.dataItems = await this.$store.getters[
      "annotationData/annotationDataArray"
    ];
  },
  methods: {
    queryFlagRemove(item) {
      (this as any).queryFlagSelect.splice(
        (this as any).queryFlagSelect.indexOf(item),
        1,
      );
    },
    candFlagRemove(item) {
      (this as any).candFlagSelect.splice(
        (this as any).candFlagSelect.indexOf(item),
        1,
      );
    },
    async updateFilter(): Promise<void> {
      const origItems = await this.$store.getters[
        "annotationData/annotationDataArray"
      ];
      const pred = this._.overEvery(this.predFuncs);
      let res = this._.chain(origItems).filter(pred).value();
      console.log(res.length);
      if (this.useQueryFlagFilter) {
        res = this._.chain(res)
          .filter((e) => {
            const good = this._.some(this.queryFlagSelect, (flag) =>
              e.flags.includes(flag),
            );
            return good;
          })
          .value();
        console.log(res.length);
      }
      if (this.useCandFlagFilter) {
        res = this._.chain(res)
        .filter((e) => {
          const good = this._.some(this.candFlagSelect, (flag) => {
            const candFlags = this._.chain(e.cand_flags).values().flatten().uniq().value();
            return candFlags.includes(flag);
          })
        })
      }
      this.dataItems = res;
    },
  },
});
</script>
