<template lang="pug">
div
  v-list-item(three-line)
    v-list-item-content
      v-list-item-title.pb-2
        a(:href="item.ent_id", target="_blank", @click.stop)
          span.text-h5 {{ item.ent_term }}
      tooltip(:docs="td.entId", position="top", :show-underline="false")
        v-list-item-subtitle
          span
            | id:
            | &nbsp;
            span.font-weight-bold {{ item.ent_id }}
      v-list-item-subtitle
        tooltip(
          :docs="td.entSynonyms",
          position="top",
          :show-underline="false"
        )
          span
            | synonyms:
            | &nbsp;
            span.font-weight-bold {{ item.synonyms }}
      v-list-item-subtitle
        tooltip(
          :docs="td.entMatchedTerms",
          position="top",
          :show-underline="false"
        )
          span
            | matched_terms:
            | &nbsp;
            span.font-weight-bold {{ item.matched_terms }}
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";
import * as types from "@/types/types";
import * as td from "@/resources/tooltip-docs";

export default Vue.extend({
  name: "SelectItem",
  components: {
    //
  },
  props: {
    item: {
      type: Object as PropType<types.VectorEnt>,
      required: true,
    },
    traitId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      td: td,
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
