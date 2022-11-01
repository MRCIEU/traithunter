<template lang="pug">
div
  div(v-for="(item, idx) in providers", :key="idx")
    v-btn(
      :href="item.url_fn(traitTerm)",
      text,
      target="_blank",
      color="teal lighten-2"
    )
      v-icon mdi-magnify
      span {{ item.label }}
    br
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "ExternalLookup",
  components: {
    //
  },
  props: {
    traitTerm: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      providers: [
        {
          name: "ols",
          label: "Ontology Lookup Service",
          url_fn: function (query: string): string {
            const url = `https://ebi.ac.uk/ols/search?q=${query}`;
            return url;
          },
        },
        {
          name: "epigraphdb",
          label: "EpiGraphDB (meta-nodes)",
          url_fn: function (query: string): string {
            const url = `https://epigraphdb.org/search?meta_node&q=${query}`;
            return url;
          },
        },
        {
          name: "google",
          label: "Google",
          url_fn: function (query: string): string {
            const url = `https://google.com/search?q=${query}`;
            return url;
          },
        },
      ],
    };
  },
  computed: {
    //
  },
  mounted() {
    //
  },
  methods: {},
});
</script>

<style scoped>
.cand-select {
  max-height: 750px;
  overflow-y: scroll;
}
</style>
