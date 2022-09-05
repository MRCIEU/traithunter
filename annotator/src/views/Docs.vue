<template lang="pug">
v-container
  v-row
    v-col(cols="6")
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
    v-col(cols="6")
      v-card.py-5
        v-card-title Types
        v-card-text
          vue-markdown(:source="docs.docsTypes", :breaks="false")
          prism(language="typescript", :code="typeRaw")
      v-divider
</template>

<script lang="ts">
import Vue from "vue";
import * as docs from "@/resources/docs";
import typeRaw from "!!raw-loader!@/types/types";
import Prism from "vue-prism-component";
import "prismjs/components/prism-typescript";

export default Vue.extend({
  name: "Docs",
  components: {
    Prism,
  },
  data() {
    return {
      docs: docs,
      typeRaw: typeRaw,
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
