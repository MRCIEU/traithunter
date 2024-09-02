<template lang="pug">
v-container
  v-card
    v-card-title
      h2 Data Explorer (pilot)
    v-card-text
      vue-markdown(:source="docs.dataExplorerDoc")
      v-row
        v-col
          v-select.px-4(
            v-model="dictionary",
            :items="dictionaryOptions",
            label="Select dictionary"
          )
        v-col
          v-btn(@click="updateTable", color="primary") Update table
      v-divider
      data-explorer-table(:items="dataItems")
</template>

<script lang="ts">
import Vue from "vue";

import * as backend from "@/funcs/backend-requests";
import * as docs from "@/resources/docs/docs";

import DataExplorerTable from "@/components/tables/DataExplorerTable.vue";

export default Vue.extend({
  name: "DataExplorer",
  components: {
    DataExplorerTable,
  },
  data() {
    return {
      docs: docs,
      dataItems: [],
      dictionary: "opengwas",
      dictionaryOptions: [],
    };
  },
  computed: {
    //
  },
  watch: {
    //
  },
  mounted: async function (): Promise<void> {
    this.dictionaryOptions = await backend.getDictionaryOptions();
    await this.updateTable();
  },
  methods: {
    async updateTable(): Promise<void> {
      this.dataItems = await backend.getEntityInfoList(this.dictionary);
    },
  },
});
</script>
