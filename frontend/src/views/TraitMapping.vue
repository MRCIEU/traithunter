<template lang="pug">
v-card
  v-card-title
    h2 Trait mapping
  div
    h3 Configure search parameters
    v-form
      v-row
        v-col
          v-subheader Source entity
          v-select.px-4(
            v-model="dictionary",
            label="Select dictionary",
            :items="dictionaryOptions"
          )
          v-select.px-4(
            v-model="entityToSearch",
            :disabled="entSelectDisabled",
            :label="entSelectLabel"
          )
          v-subheader Target entity
        v-col
          v-subheader Other parameters
          v-select.px-4(
            v-model="embeddingType",
            label="Select embedding model",
            :items="embeddingTypeOptions"
          )
          v-subheader Top K neighbors
          .pt-4
          .pt-4
          v-slider.px-4(
            ticks="always",
            thumb-label="always",
            v-model="topK",
            :min="10",
            :max="40",
            :step="5"
          )
      v-btn(@click="submit", color="primary") Submit
  v-divider.py-5
  div
    h3 Results
</template>

<script lang="ts">
import Vue from "vue";
import * as backend from "@/funcs/backend-requests";

export default Vue.extend({
  name: "TraitMapping",
  components: {
    //
  },
  data() {
    return {
      entityToSearch: null,
      entityOptions: [],
      dictionary: null,
      dictionaryOptions: [],
      embeddingType: null,
      embeddingTypeOptions: ["bge", "llama3"],
      topK: 15,
    };
  },
  computed: {
    entSelectDisabled() {
      return true;
    },
    entSelectLabel() {
      const ready = "Search and select an entity";
      const notReady = "Choose a dictionary first";
      return ready;
    },
  },
  watch: {
    //
  },
  mounted: async function (): Promise<void> {
    this.dictionaryOptions = await backend.getDictionaryOptions();
  },
  methods: {
    async submit(): Promise<void> {
      return null;
    }
  },
});
</script>
