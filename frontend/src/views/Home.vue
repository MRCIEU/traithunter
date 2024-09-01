<template lang="pug">
v-container
  v-card
    v-card-title
      h2 Trait Hunter
  v-divider
  trait-mapping
</template>

<script lang="ts">
import Vue from "vue";

import TraitMapping from "./TraitMapping.vue";

export default Vue.extend({
  name: "Home",
  components: {
    TraitMapping,
  },
  data() {
    return {
      //
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
