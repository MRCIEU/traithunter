<template lang="pug">
v-card
  v-card-title
  v-data-table(:headers="headers", :items="items")
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "KnnTable",
  props: {
    items: Array,
  },
  data() {
    return {
      headers: [
        {
          text: "Entity ID",
          value: "ent_id",
        },
        {
          text: "Entity label",
          value: "ent_term",
        },
        {
          text: "Dictionary",
          value: "dictionary",
        },
        {
          text: "Cosine similarity score",
          value: "score",
        },
      ],
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
