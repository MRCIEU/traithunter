<template lang="pug">
v-container
  v-card
    v-card-title
      h2 Trait Hunter
    v-card-text
      vue-markdown(:source="docs.topDoc")
  v-divider
  v-tabs(v-model="tab", grow)
    v-tab Trait Mapping
    v-tab API example
  v-tabs-items(v-model="tab")
    v-tab-item
      trait-mapping
    v-tab-item
      vue-markdown(:source="tutorialDocs.traitMappingTutorial")
      prism(language="python", :code="tutorialDocs.pingSnippet.trim()")
      prism(language="python", :code="tutorialDocs.traitMappingSnippet.trim()")
</template>

<script lang="ts">
import Vue from "vue";
import Prism from "vue-prism-component";
import "prismjs/components/prism-python";

import TraitMapping from "@/components/TraitMapping.vue";

import * as docs from "@/resources/docs/docs";
import * as tutorialDocs from "@/resources/docs/api-examples";

export default Vue.extend({
  name: "Home",
  components: {
    TraitMapping,
    Prism,
  },
  data() {
    return {
      docs: docs,
      tutorialDocs: tutorialDocs,
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
