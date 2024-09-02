<template lang="pug">
v-container
  v-card
    v-card-title
      h2 Pairwise cosine similarities
    v-card-text
      p
        vue-markdown(:source="docs.pairwiseDoc")
      h3 Step 1: Search for entities to include in the comparison
      v-row
        v-col(cols="2")
          v-select.px-4(
            v-model="dictionary",
            :items="dictionaryOptions",
            label="Select dictionary"
          )
        v-col(cols="8")
          v-autocomplete.px-4(
            v-model="entityToSearch",
            :disabled="entSelectDisabled",
            :label="entSelectLabel",
            :search-input.sync="entityAcQuery",
            :loading="isEntitySearchLoading",
            :items="entityOptions",
            item-text="ent_term",
            :return-object="true"
          )
            template(v-slot:no-data)
              v-list-item
                v-list-item-title
                  span Type to search entity by its label
            template(v-slot:selection="{ attr, on, item, selected }")
              v-chip(v-bind="attr", :input-value="selected", v-on="on")
                span
                  i {{ item.dictionary }}
                |
                span.pl-4 {{ item.ent_id }}
                |
                span.pl-4
                  b {{ item.ent_term }}
            template(v-slot:item="{ item }")
              entity-candidate(
                :ent-id="item.ent_id",
                :ent-term="item.ent_term",
                :dictionary="item.dictionary"
              )
        v-col
          v-btn(:disabled="includeBtnDisabled", @click="addEntToList") Add to list
      div(v-if="pairwiseEntities.length > 0")
        v-subheader Included entities
        v-item-group(multiple)
          v-item(
            v-for="(item, idx) in pairwiseEntities",
            :key="idx",
            v-slot="{ active, toggle }"
          )
            v-chip(active-class="purple--text", :input-value="active")
              entity-span(
                :ent-id="item.ent_id",
                :ent-term="item.ent_term",
                :dictionary="item.dictionary"
              )
      v-divider
      h3 Step 2: Configure parameters
      v-subheader Other parameters
      v-row
        v-col(cols="4")
          v-select.px-4(
            v-model="embeddingType",
            label="Select embedding model",
            :items="embeddingTypeOptions"
          )
      .d-flex.justify-center.mb-6
        v-btn(
          :disabled="submitBtnDisabled",
          @click="submit",
          color="primary",
          large
        ) Submit
      v-divider
      div(v-if="pairwiseResults.length > 0")
        h3 Results
        pairwise-table(:items="pairwiseResults")
</template>

<script lang="ts">
import Vue from "vue";
import EntityCandidate from "@/components/widgets/EntityCandidate.vue";
import EntitySpan from "@/components/widgets/EntitySpan.vue";
import PairwiseTable from "@/components/tables/PairwiseTable.vue";

import * as backend from "@/funcs/backend-requests";
import * as docs from "@/resources/docs/docs";

export default Vue.extend({
  name: "Pairwise",
  components: {
    EntityCandidate,
    EntitySpan,
    PairwiseTable,
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
      dictionaryOptions: [],
      embeddingType: null,
      embeddingTypeOptions: ["bge", "llama3"],
      // results
      pairwiseEntities: [],
      pairwiseResults: [],
    };
  },
  computed: {
    entSelectDisabled(): boolean {
      return !this.dictionary;
    },
    includeBtnDisabled(): boolean {
      const enabled = this.entityToSearch;
      return !enabled;
    },
    submitBtnDisabled(): boolean {
      const enabled = this.pairwiseEntities.length >= 2 && this.embeddingType;
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
    addEntToList() {
      if (!this.pairwiseEntities.includes(this.entityToSearch)) {
        this.pairwiseEntities.push(this.entityToSearch);
      }
    },
    async submit(): Promise<void> {
      this.pairwiseResults = await backend.postPairwise(
        this.pairwiseEntities,
        this.embeddingType,
      );
    },
  },
});
</script>
