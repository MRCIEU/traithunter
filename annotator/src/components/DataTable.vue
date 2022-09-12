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
        h3 Flag filter
        v-subheader When enabled, will show items that contain ANY of the included flags (they first need to exist in the metadata settings)
        v-checkbox(label="Enable flag filter", v-model="useFlagFilter")
        v-combobox(
          v-model="flagSelect",
          :items="flagItems",
          chips,
          clearable,
          label="flags",
          multiple,
          preprend-icon="mdi-filter-variant",
          solor
        )
          template(v-slot:selection="{ attrs, item, select, selected }")
            v-chip(
              v-bind="attrs",
              :input-value="selected",
              close,
              @click="select",
              @click:close="flagRemove(item)"
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
      useFlagFilter: false,
      flagSelect: [],
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
    flagRemove(item) {
      (this as any).flagSelect.splice(
        (this as any).flagSelect.indexOf(item),
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
      if (this.useFlagFilter) {
        res = this._.chain(res)
          .filter((e) => {
            const good = this._.some(this.flagSelect, (flag) =>
              e.flags.includes(flag),
            );
            return good;
          })
          .value();
        console.log(res.length);
      }
      this.dataItems = res;
    },
  },
});
</script>
