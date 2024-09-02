<template lang="pug">
v-card
  v-card-title
  v-data-table(:headers="headers", :items="items", :items-per-page="15")
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "DataExplorerTable",
  components: {
    //
  },
  props: {
    items: Array,
  },
  data() {
    return {
      headers: [
        {
          text: "Entity id",
          value: "id",
        },
        {
          text: "Entity label",
          value: "label",
        },
        {
          text: "Description",
          value: "description",
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
