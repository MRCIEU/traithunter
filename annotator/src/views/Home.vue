<template lang="pug">
v-container
  IO
  .py-5
  div(v-if="showTable")
    data-table
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
