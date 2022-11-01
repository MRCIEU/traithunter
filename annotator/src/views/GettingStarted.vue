<template lang="pug">
v-container(fluid)
  .px-5.mx-5
    v-card.py-5
      v-card-title Getting started
      v-card-text
        vue-markdown(:source="docs.docsGettingStarted", :breaks="false")
</template>

<script lang="ts">
import Vue from "vue";
import * as docs from "@/resources/docs";

export default Vue.extend({
  name: "GettingStarted",
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
