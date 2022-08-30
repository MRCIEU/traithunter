<template lang="pug">
div
  vue-markdown(:source="docs.gettingStarted", :breaks="false")
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
