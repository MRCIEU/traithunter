<template lang="pug">
v-container
  h1 File settings
  IO
  .py-5
  h1 Metadata settings
  div
    span Flags / tags for query items
    br
    span Flags / tags for mapping items
  .py-5
  h1 Annotation for mapping results
  div(v-if="showTable")
    data-table
    v-btn.floating-button(color="success", x-large)
      v-icon mdi-content-save
      | Save
</template>

<script lang="ts">
import Vue from "vue";
import IO from "@/components/IO.vue";
import DataTable from "@/components/DataTable.vue";

export default Vue.extend({
  name: "Home",
  components: {
    IO,
    DataTable,
  },
  data() {
    return {};
  },
  computed: {
    showTable(): boolean {
      return this.$store.state.annotationData.data != null ? true : false;
    },
  },
  methods: {},
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
