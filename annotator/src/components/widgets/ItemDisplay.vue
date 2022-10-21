<template lang="pug">
div(v-if="itemData")
  v-card(:color="cardBg")
    v-card-text
      v-card-title
        span
          span.font-weight-thin {{ idx }}
          | &nbsp;
          span {{ traitTerm }}
      v-expansion-panels(v-model="panelState", multiple)
        v-expansion-panel
          v-expansion-panel-header Annotation
          v-expansion-panel-content
            v-row
              v-col(cols="3")
                h4 Basic info
                v-subheader Basic information about the query item
                json-viewer(
                  theme="json-viewer-gruvbox-dark",
                  :value="traitQueryInfo",
                  :expand-depth="3"
                )
                h4 External lookup
                v-subheader Look up about the query item in external resources
                external-lookup(:traitTerm="traitTerm")
              v-col(cols="5")
                h4 Candidate selection
                v-subheader Select suitable candidates from all candidates identified in the mapping strategies
                .cand-select
                  div(v-for="(id, idx) in candidateOptions", :key="idx")
                    span Candidate {{ idx }}
                    v-checkbox(
                      :label="id",
                      :value="id",
                      v-model="candidateSelect"
                    )
                      template(v-slot:label)
                        select-item(
                          :item="candidateInfo[id]",
                          :trait-id="traitId"
                        )
                    cand-flags.ml-5.pl-5(
                      :trait-id="traitId",
                      :ent-id="id"
                    )
                    v-divider
              v-col(cols="4")
                h4 Notes
                v-subheader Insert notes for future reference
                v-textarea(
                  v-model="notes",
                  auto-grow,
                  filled,
                  label="Insert notes for future reference"
                )
                h4 Flags for this query item
                v-subheader Add flags (they first need to exist in the metadata settings, and anything unregistered will be discarded)
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
                  template(
                    v-slot:selection="{ attrs, item, select, selected }"
                  )
                    v-chip(
                      v-bind="attrs",
                      :input-value="selected",
                      close,
                      @click="select",
                      @click:close="flagRemove(item)"
                    )
                      span {{ item }} &nbsp;
                h4 External picks
                v-subheader Add external alternative picks
                external-selection(:traitId="traitId")
        v-expansion-panel
          v-expansion-panel-header Mapping results
          v-expansion-panel-content
            v-row
              v-col(cols="4")
                h4 Equivalence mapping results
                div(
                  v-for="(item, idx) in itemData.equivalence_res",
                  :key="idx"
                )
                  ent-item(:item="item")
              v-col(cols="4")
                h4 Composite mapping results
                div(v-for="(item, idx) in itemData.composite_res", :key="idx")
                  ent-item(:item="item")
</template>

<script lang="ts">
import Vue from "vue";
import SelectItem from "@/components/widgets/SelectItem.vue";
import CandFlags from "@/components/widgets/CandFlags.vue";
import EntItem from "@/components/widgets/EntItem.vue";
import ExternalSelection from "@/components/widgets/ExternalSelection.vue";
import ExternalLookup from "@/components/widgets/ExternalLookup.vue";
import * as types from "@/types/types";

export default Vue.extend({
  name: "ItemDisplay",
  components: {
    SelectItem,
    CandFlags,
    EntItem,
    ExternalSelection,
    ExternalLookup,
  },
  props: {
    traitId: {
      type: String,
      required: true,
    },
    traitTerm: {
      type: String,
      required: true,
    },
    idx: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      itemData: null,
      panelState: [0],
    };
  },
  computed: {
    traitQueryInfo(): any {
      const res = {
        trait_id: this.itemData.trait_id,
        trait_term: this.itemData.trait_term,
        trait_term_query: this.itemData.trait_term_query,
        trait_basic_info: this.itemData.trait_basic_info,
      };
      return res;
    },
    cardBg(): string {
      const odd = "blue-grey lighten-5";
      const even = "brown lighten-5";
      const res = this.idx % 2 == 0 ? even : odd;
      return res;
    },
    candidateOptions: {
      get(): Array<string> {
        return this._.chain(this.itemData.candidates)
          .map((e) => e.ent_id)
          .value();
      },
    },
    candidateSelect: {
      get(): Array<string> {
        return this._.chain(this.itemData.selection).value();
      },
      async set(newVal): Promise<void> {
        await this.$store.dispatch("annotationData/updateItemProp", {
          id: this.traitId,
          prop: "selection",
          value: newVal,
        });
      },
    },
    notes: {
      get(): string {
        return this._.chain(this.itemData.notes).value();
      },
      async set(newVal: string) {
        await this.$store.dispatch("annotationData/updateItemProp", {
          id: this.traitId,
          prop: "notes",
          value: newVal,
        });
      },
    },
    candidateInfo(): any {
      return this._.chain(this.itemData.candidates)
        .reduce((a, b) => ({ ...a, [b["ent_id"]]: b }), {})
        .value();
    },
    flagItems(): Array<string> {
      const flags = this.$store.state.annotationData.metadata.flags;
      const res = this._.chain(flags)
        .map((e) => e.name)
        .value() as Array<string>;
      return res;
    },
    flagSelect: {
      get(): Array<string> {
        const flags = this.$store.state.annotationData.data[this.traitId].flags;
        return flags as Array<string>;
      },
      async set(newVal: Array<string>) {
        const flags = this._.chain(newVal)
          .filter((e) => this.flagItems.includes(e))
          .value();
        await this.$store.dispatch("annotationData/updateItemProp", {
          id: this.traitId,
          prop: "flags",
          value: flags,
        });
      },
    },
  },
  mounted() {
    this.itemData = this.$store.state.annotationData.data[this.traitId];
  },
  methods: {
    flagRemove(item) {
      (this as any).flagSelect.splice(
        (this as any).flagSelect.indexOf(item),
        1,
      );
    },
  },
});
</script>

<style scoped>
.cand-select {
  max-height: 750px;
  overflow-y: scroll;
}
</style>
