<template lang="pug">
v-card
  v-card-title
    h2 Trait mapping
  v-card-text
    h3 Configure search parameters
    vue-markdown(:source="docs.traitMappingDoc")
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
              v-chip(v-bind="attr", :input-value="selected", v-on="on")
                entity-span(
                  :ent-id="item.ent_id",
                  :ent-term="item.ent_term",
                  :dictionary="item.dictionary"
                )
            template(v-slot:item="{ item }")
              entity-candidate(
                :ent-id="item.ent_id",
                :ent-term="item.ent_term",
                :dictionary="item.dictionary"
              )
          v-subheader Target entity
          v-select.px-4(
            v-model="dictionaryTarget",
            label="Select dictionary of the target entities",
            :items="dictionaryOptions"
          )
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
      .d-flex.justify-center.mb-6
        v-btn(
          :disabled="submitBtnDisabled",
          @click="submit",
          color="primary",
          large
        ) Submit
    v-divider.py-5
    div(v-if="knnItems.length > 0")
      h3 Results
      knn-table(:items="knnItems")
</template>

<script lang="ts">
import Vue from "vue";
import EntityCandidate from "@/components/widgets/EntityCandidate.vue";
import EntitySpan from "@/components/widgets/EntitySpan.vue";
import KnnTable from "@/components/tables/KnnTable.vue";

import * as backend from "@/funcs/backend-requests";
import * as docs from "@/resources/docs/docs";

export default Vue.extend({
  name: "TraitMapping",
  components: {
    EntityCandidate,
    EntitySpan,
    KnnTable,
  },
  data() {
    return {
      docs: docs,
      // entity search things ----
      entityToSearch: null,
      entityAcQuery: null,
      entityOptions: [],
      isEntitySearchLoading: false,
      // entity search things ----
      dictionary: null,
      dictionaryTarget: null,
      dictionaryOptions: [],
      embeddingType: null,
      embeddingTypeOptions: ["bge", "llama3"],
      topK: 15,
      // results
      knnItems: [],
    };
  },
  computed: {
    entSelectDisabled(): boolean {
      return !this.dictionary;
    },
    submitBtnDisabled(): boolean {
      const enabled =
        this.entityToSearch &&
        this.dictionary &&
        this.dictionaryTarget &&
        this.topK &&
        this.embeddingType;
      return !enabled;
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
      this.knnItems = await backend.getKnn(
        this.entityToSearch,
        this.dictionary,
        this.dictionaryTarget,
        this.topK,
        this.embeddingType,
      );
    },
  },
});
</script>
