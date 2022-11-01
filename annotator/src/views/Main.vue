<template lang="pug">
v-container(fluid)
  div(v-if="!initDone")
    h1 Getting started
    getting-started
  v-expansion-panels(v-model="panelState", multiple)
    v-expansion-panel
      v-expansion-panel-header
        h1
          span File settings & operations
          | &nbsp;
          | &nbsp;
          | &nbsp;
          | &nbsp;
      v-expansion-panel-content
        file-settings
        v-divider
        .py-3(v-if="initDone")
          v-btn.mx-2(color="success", x-large, @click="save")
            tooltip(:docs="docs.btnSave", :nudge-bottom="20")
              v-icon mdi-content-save
              | &nbsp;
              span Save
          v-btn.mx-2(color="info", x-large, @click="flatDataExport")
            tooltip(:docs="docs.btnExport", :nudge-bottom="20")
              v-icon mdi-export-variant
              | &nbsp;
              span Export flat file
    .py-5
    v-expansion-panel(v-if="initDone")
      v-expansion-panel-header
        h1 Metadata settings
      v-expansion-panel-content
        metadata
    .py-5
    v-expansion-panel(v-if="initDone")
      v-expansion-panel-header
        h1 Annotation for mapping results
      v-expansion-panel-content
        div(v-if="initDone")
          data-table
    div(v-if="initDone")
      v-btn.floating-button(color="success", x-large, @click="save")
        tooltip(:docs="docs.btnSave", position="top", :nudge-top="20")
          v-icon mdi-content-save
          | &nbsp;
          span Save
</template>

<script lang="ts">
import Vue from "vue";
import FileSettings from "@/components/FileSettings.vue";
import DataTable from "@/components/DataTable.vue";
import Metadata from "@/components/Metadata.vue";
import GettingStarted from "@/components/GettingStarted.vue";
import * as docs from "@/resources/docs";
import * as io from "@/funcs/io";
import * as types from "@/types/types";

export default Vue.extend({
  name: "Main",
  components: {
    FileSettings,
    DataTable,
    Metadata,
    GettingStarted,
  },
  data() {
    return {
      panelState: [0],
      docs: docs,
    };
  },
  computed: {
    initDone(): boolean {
      return this.$store.state.io.initDone;
    },
  },
  watch: {
    initDone(val): void {
      if (val) {
        this.panelState = this._.chain(this.panelState.concat([1, 2]))
          .uniq()
          .value();
      }
    },
  },
  methods: {
    async save(): Promise<void> {
      const outputFile = this.$store.state.io.output;
      const exportData: types.AnnotationDataExport =
        this.$store.getters["annotationData/annotationDataExport"];
      await io.save(outputFile, exportData);
      const lastSaveTime = new Date().toLocaleString();
      await this.$store.dispatch("io/updateSaveTime", lastSaveTime);
    },
    async flatDataExport(): Promise<void> {
      const pickerOpts = {
        suggestedName: "annotation_results_flat.json",
        types: [
          {
            description: "JSON file",
            accept: {
              "application/*": [".json"],
            },
          },
        ],
      };
      const outputFile = await window.showSaveFilePicker(pickerOpts);
      const exportData = await this.$store.getters[
        "annotationData/flatDataExport"
      ];
      const writableStream = await outputFile.createWritable();
      await writableStream.write(JSON.stringify(exportData));
      await writableStream.close();
    },
  },
});
</script>

<style scoped>
.floating-button {
  position: fixed;
  right: 20px;
  bottom: 100px;
  z-index: 120;
}
</style>
