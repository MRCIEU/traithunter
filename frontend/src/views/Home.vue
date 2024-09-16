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
</template>

<script lang="ts">
import Vue from "vue";

import TraitMapping from "@/components/TraitMapping.vue";

import * as docs from "@/resources/docs/docs";

export default Vue.extend({
  name: "Home",
  components: {
    TraitMapping,
  },
  data() {
    return {
      docs: docs,
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
