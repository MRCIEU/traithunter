<template lang="pug">
v-container
  v-card
    v-card-title
      h2 Trait Hunter
    v-card-text
      h3 About this platform
      vue-markdown(:source="docs.aboutDesc")
      v-divider
      h3 Information about curated data
      h4 Curated indices
        div(v-if="infoEsStatus")
          json-viewer(
            theme="json-viewer-gruvbox-dark",
            :value="infoEsStatus",
            :expand-depth="4"
          )
      h4 Size of documents
        div(v-if="infoDocSizes")
          json-viewer(
            theme="json-viewer-gruvbox-dark",
            :value="infoDocSizes",
            :expand-depth="4"
          )
</template>

<script lang="ts">
import Vue from "vue";
import * as docs from "@/resources/docs/docs";

import * as backend from "@/funcs/backend-requests";

export default Vue.extend({
  name: "About",
  components: {
    //
  },
  data() {
    return {
      docs: docs,
      dictionary: [],
      infoEsStatus: null,
      infoDocSizes: null,
    };
  },
  computed: {
    //
  },
  watch: {
    //
  },
  mounted: async function (): Promise<void> {
    this.dictionary = await backend.getDictionaryOptions();
    this.infoEsStatus = await backend.getEsStatus();
    this.infoDocSizes = await Promise.all(
      this._.chain(this.dictionary)
        .map(async function (e) {
          const dictionaryLength = await backend.getDictionaryLength(e);
          const res = {
            index: e,
            document_size: dictionaryLength,
          };
          return res;
        })
        .value(),
    );
  },
  methods: {
    //
  },
});
</script>
