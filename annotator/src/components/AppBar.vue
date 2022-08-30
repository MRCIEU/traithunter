<template lang="pug">
v-app-bar#navbar(app, dense, flat)
  v-toolbar-title
    div(v-if="!isMain")
      tooltip(:docs="`Back to the main page`", :show-underline="false")
        v-btn(href="/", text, dark)
          span.ml-3 {{ appTitle }}
    div(v-else)
      span.ml-3 {{ appTitle }}
  span.px-5
  tooltip(:docs="`Documentation`", :show-underline="false")
    v-btn(href="/docs", text, dark, target="_blank")
      span Docs
  v-spacer
  v-sheet(color="transparent")
    .py-2
    a(href="https://mrcieu.github.io", target="_blank")
      img(alt="", src="@/assets/MRC_IEU_Bristol_White.svg", height="59px")
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  name: "AppBar",
  data: () => ({
    appTitle: "Ontology harmonization annotator",
  }),
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
    isMain() {
      return this.currentRouteName == "Main";
    },
  },
});
</script>

<style scoped>
#navbar {
  background-color: rgba(51, 122, 183, 0.8);
  color: white;
  backdrop-filter: blur(5px);
}
</style>
