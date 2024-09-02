<template lang="pug">
div
  span
    i {{ dictionary }}
  |
  span.pl-4 {{ entId }}
  |
  span.pl-4
    b {{ entTerm }}
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "EntityCandidate",
  props: {
    entId: String,
    entTerm: String,
    dictionary: String,
  },
  computed: {
    //
  },
  methods: {
    //
  },
});
</script>
