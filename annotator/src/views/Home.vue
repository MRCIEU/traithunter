<template lang="pug">
v-container
  h1 File settings
  IO
  .py-5
  h1 Metadata settings
  div(v-if="inputDone")
    metadata
  .py-5
  h1 Annotation for mapping results
  div(v-if="inputDone")
    data-table
    v-btn.floating-button(
      color="success",
      x-large,
      @click="save",
      :disabled="!outputDone"
    )
      v-icon mdi-content-save
      | Save
</template>

<script lang="ts">
import Vue from "vue";
import IO from "@/components/IO.vue";
import DataTable from "@/components/DataTable.vue";
import Metadata from "@/components/Metadata.vue";
import * as io from "@/funcs/io";
import * as types from "@/types/types";

export default Vue.extend({
  name: "Home",
  components: {
    IO,
    DataTable,
    Metadata,
  },
  data() {
    return {};
  },
  computed: {
    inputDone(): boolean {
      return this.$store.state.annotationData.data != null ? true : false;
    },
    outputDone(): boolean {
      return this.$store.state.io.output != null;
    },
  },
  methods: {
    async save(): Promise<void> {
      const outputFile = this.$store.state.io.output;
      const exportData: types.AnnotationDataExport = {
        metadata: this.$store.state.annotationData.metadata,
        data: this.$store.state.annotationData.data,
      };
      await io.save(outputFile, exportData);
      const lastSaveTime = new Date().toLocaleString();
      await this.$store.dispatch("io/updateSaveTime", lastSaveTime);
    },
  },
});
</script>

<style scoped>
.floating-button {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 120;
}
</style>
