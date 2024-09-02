<template lang="pug">
v-card
  v-card-title
  v-data-table(:headers="headers", :items="items")
    template(v-slot:item.entity_a="{ item }")
      entity-candidate(
        :ent-id="item.entity_a.id",
        :dictionary="item.entity_a.dictionary"
      )
    template(v-slot:item.entity_b="{ item }")
      entity-candidate(
        :ent-id="item.entity_b.id",
        :dictionary="item.entity_b.dictionary"
      )
</template>

<script lang="ts">
import Vue from "vue";
import EntityCandidate from "@/components/widgets/EntityCandidate.vue";

export default Vue.extend({
  name: "PairwiseTable",
  components: {
    EntityCandidate,
  },
  props: {
    items: Array,
  },
  data() {
    return {
      headers: [
        {
          text: "Entity A",
          value: "entity_a",
        },
        {
          text: "Entity B",
          value: "entity_b",
        },
        {
          text: "Cosine similarity score",
          value: "similarity_score",
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
