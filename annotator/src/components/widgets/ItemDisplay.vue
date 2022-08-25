<template lang="pug">
div(v-if="itemData")
  v-card
    v-card-text
      v-card-title {{ itemData.trait_term }}
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
            v-model="selectId"
          )
            template(v-slot:label)
              div(slot="label")
                v-list-item(three-line)
                  v-list-item-content
                    v-list-item-title
                      a(:href="id", target="_blank", @click.stop) {{ candidateInfo[id].ent_term }}
                    v-list-item-subtitle id: {{ id }}
                    v-list-item-subtitle
                      span
                        | vector_term:
                        span.font-weight-bold {{ candidateInfo[id].vector_term }}
                    v-list-item-subtitle primary_term: {{ candidateInfo[id].primary_term }}
        v-col(cols="4")
          h4 Notes
          v-textarea(
            v-model="notes",
            auto-grow,
            filled,
            label="Insert notes for future reference (optional)"
          )
      v-row
        v-col(cols="6")
          h4 Equivalence mapping results
        v-col(cols="6")
          h4 Composite mapping results
</template>

<script lang="ts">
import Vue from "vue";
import * as types from "@/types/types";

export default Vue.extend({
  name: "ItemDisplay",
  components: {
    //
  },
  props: {
    traitId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      itemData: null,
      notes: "",
      selectId: [],
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
    candidateOptions() {
      return this._.chain(this.itemData.candidates)
        .map((e) => e.ent_id)
        .value();
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
