<template lang="pug">
v-container
  v-tabs(v-model="tab", grow)
    v-tab Pairwise cosine similarties
    v-tab API example
  v-tabs-items(v-model="tab")
    v-tab-item
      pairwise
    v-tab-item
</template>

<script lang="ts">
import Vue from "vue";

import Pairwise from "@/components/Pairwise.vue";
export default Vue.extend({
  name: "PairwiseView",
  components: {
    Pairwise,
  },
  data() {
    return {
      tab: 0,
    };
  },
  computed: {
    //
  },
  watch: {
    //
  },
  mounted: async function (): Promise<void> {
    //
  },
  methods: {
    //
  },
});
</script>
