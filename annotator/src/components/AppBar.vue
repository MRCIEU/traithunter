<template lang="pug">
v-app-bar#navbar(app, dense, flat)
  v-toolbar-title
    tooltip(:docs="`Back to the main page`", :show-underline="false")
      v-btn(href="/", text, dark)
      span.ml-3 {{ appTitle }}
  span.px-1
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
  },
});
</script>

<style scoped>
#navbar {
  background-color: rgba(21, 62, 62, 0.8);
  color: white;
  backdrop-filter: blur(5px);
}
</style>
