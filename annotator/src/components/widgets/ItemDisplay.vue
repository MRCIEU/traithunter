<template lang="pug">
div(v-if="itemData")
  v-card
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
                json-viewer(
                  theme="json-viewer-gruvbox-dark",
                  :value="traitQueryInfo"
                )
              v-col(cols="5")
                h4 Candidate selection
                v-checkbox(
                  v-for="(id, idx) in candidateOptions",
                  :key="idx",
                  :label="id",
                  :value="id",
                  v-model="candidateSelect"
                )
                  template(v-slot:label)
                    select-item(:item="candidateInfo[id]")
              v-col(cols="4")
                h4 Notes
                v-textarea(
                  v-model="notes",
                  auto-grow,
                  filled,
                  label="Insert notes for future reference (optional)"
                )
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
import EntItem from "@/components/widgets/EntItem.vue";
import * as types from "@/types/types";

export default Vue.extend({
  name: "ItemDisplay",
  components: {
    SelectItem,
    EntItem,
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
      notes: "",
      panelState: [0],
    };
  },
  computed: {
    traitQueryInfo() {
      const res = {
        trait_id: this.itemData.trait_id,
        trait_term: this.itemData.trait_term,
        trait_term_query: this.itemData.trait_term_query,
        phenotype: this.itemData.phenotype,
        dataset: this.itemData.dataset,
      };
      return res;
    },
    candidateOptions: {
      get() {
        return this._.chain(this.itemData.candidates)
          .map((e) => e.ent_id)
          .value();
      },
    },
    candidateSelect: {
      get() {
        return this._.chain(this.itemData.selection).value();
      },
      async set(newVal) {
        await this.$store.dispatch("annotationData/updateCandidateSelect", {
          id: this.traitId,
          selection: newVal,
        });
      },
    },
    candidateInfo() {
      return this._.chain(this.itemData.candidates)
        .reduce((a, b) => ({ ...a, [b["ent_id"]]: b }), {})
        .value();
    },
  },
  mounted() {
    this.itemData = this.$store.state.annotationData.data[this.traitId];
  },
  methods: {
    //
  },
});
</script>
