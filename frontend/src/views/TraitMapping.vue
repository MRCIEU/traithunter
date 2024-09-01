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
          v-autocomplete.px-4(
            v-model="entityToSearch",
            :disabled="entSelectDisabled",
            :label="entSelectLabel",
            :search-input.sync="entityAcQuery",
            :loading="isEntitySearchLoading",
            :items="entityOptions",
            item-text="ent_term",
            item-value="ent_id"
          )
            template(v-slot:no-data)
              v-list-item
                v-list-item-title
                  span Type to search entity by its label
            template(v-slot:selection="{ attr, on, item, selected }")
              v-chip(
                v-bind="attr",
                :input-value="selected",
                v-on="on"
              )
                span
                  i {{ item.ent_id }}
                |
                span.pl-4 {{ item.ent_term }}
            template(v-slot:item="{ item }")
              entity-candidate(
                :ent-id="item.ent_id",
                :ent-term="item.ent_term",
                :dictionary="item.dictionary"
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
import EntityCandidate from "@/components/widgets/EntityCandidate.vue";

import * as backend from "@/funcs/backend-requests";

export default Vue.extend({
  name: "TraitMapping",
  components: {
    EntityCandidate,
  },
  data() {
    return {
      // entity search things ----
      entityToSearch: null,
      entityAcQuery: null,
      entityOptions: [],
      isEntitySearchLoading: false,
      // entity search things ----
      dictionary: null,
      dictionaryOptions: [],
      embeddingType: null,
      embeddingTypeOptions: ["bge", "llama3"],
      topK: 15,
    };
  },
  computed: {
    entSelectDisabled() {
      return !this.dictionary;
    },
    entSelectLabel() {
      const ready = "Search and select an entity";
      const notReady = "Choose a dictionary first";
      if (this.entSelectDisabled) {
        return notReady;
      } else {
        return ready;
      }
    },
  },
  watch: {
    async entityAcQuery(val): Promise<void> {
      if (!val) return;
      if (val.length < 3) return;
      if (this.isEntitySearchLoading) return;
      this.isEntitySearchLoading = true;
      this.entityOptions = await backend.getEntityOptions(val, this.dictionary);
      this.isEntitySearchLoading = false;
    },
  },
  mounted: async function (): Promise<void> {
    this.embeddingType = "bge";
    this.dictionaryOptions = await backend.getDictionaryOptions();
  },
  methods: {
    async submit(): Promise<void> {
      return null;
    },
  },
});
</script>
