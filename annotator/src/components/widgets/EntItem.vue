<template lang="pug">
div
  v-card
    v-card-title
      a(:href="item.ent_id", target="_blank", @click.stop) {{ item.ent_term }}
    v-card-text
      v-list-item(three-line)
        v-list-item-content
          v-list-item-subtitle id: {{ item.ent_id }}
          v-list-item-subtitle
            span
              | vector_term:
              span.font-weight-bold {{ item.vector_term }}
          v-list-item-subtitle primary_term: {{ item.primary_term }}
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";
import * as types from "@/types/types";

export default Vue.extend({
  name: "EntItem",
  components: {
    //
  },
  props: {
    item: {
      type: Object as PropType<types.VectorEntItem>,
      required: true,
    },
  },
  data() {
    return {
      //
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
