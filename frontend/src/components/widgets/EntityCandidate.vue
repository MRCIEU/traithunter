<template lang="pug">
v-list-item
  v-list-item-content
    div
      span
        i {{ dictionary }}
      |
      span.pl-4 {{ entId }}
    br
    span
      b {{ entTerm }}
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "EntityCandidate",
  props: {
    entId: {
      type: String,
    },
    entTerm: {
      type: String,
    },
    dictionary: {
      type: String,
    },
  },
  computed: {
    //
  },
  methods: {
    //
  },
});
</script>
