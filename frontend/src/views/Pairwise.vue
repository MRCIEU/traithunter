<template lang="pug">
v-container
  v-tabs(v-model="tab", grow)
    v-tab Pairwise cosine similarties
    v-tab API example
  v-tabs-items(v-model="tab")
    v-tab-item
      pairwise
    v-tab-item
      prism(language="python", :code="tutorialDocs.pairwiseSnippet.trim()")
</template>

<script lang="ts">
import Vue from "vue";
import Prism from "vue-prism-component";
import "prismjs/components/prism-python";

import Pairwise from "@/components/Pairwise.vue";

import * as tutorialDocs from "@/resources/docs/api-examples";

export default Vue.extend({
  name: "PairwiseView",
  components: {
    Pairwise,
    Prism,
  },
  data() {
    return {
      tab: 0,
      tutorialDocs: tutorialDocs,
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
