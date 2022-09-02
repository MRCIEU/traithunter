<template lang="pug">
v-container
  v-card.py-5
    v-card-title About
    v-card-text
      vue-markdown(:source="docs.docsAbout", :breaks="false")
  v-divider
  v-card.py-5
    v-card-title Basic usage
    v-card-text
      vue-markdown(:source="docs.docsBasicUsage", :breaks="false")
  v-divider
  v-card.py-5
    v-card-title Technical specifications
    v-card-text
      vue-markdown(:source="docs.docsTechSpecs", :breaks="false")
  v-divider
  v-card.py-5
    v-card-title Mapping strategies
    v-card-text
      vue-markdown(:source="docs.docsMappingStrategies", :breaks="false")
  v-divider
</template>

<script lang="ts">
import Vue from "vue";
import * as docs from "@/resources/docs";

export default Vue.extend({
  name: "Docs",
  components: {
    //
  },
  data() {
    return {
      docs: docs,
    };
  },
  computed: {
    //
  },
  methods: {
    //
  },
});
</script>
