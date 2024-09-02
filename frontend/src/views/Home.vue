<template lang="pug">
v-container
  v-card
    v-card-title
      h2 Trait Hunter
    v-card-text
      vue-markdown(:source="docs.topDoc")
  v-divider
  trait-mapping
</template>

<script lang="ts">
import Vue from "vue";

import TraitMapping from "./TraitMapping.vue";

import * as docs from "@/resources/docs/docs";

export default Vue.extend({
  name: "Home",
  components: {
    TraitMapping,
  },
  data() {
    return {
      docs: docs,
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
