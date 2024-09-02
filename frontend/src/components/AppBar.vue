<template lang="pug">
v-app-bar#navbar(app, dense, flat)
  v-toolbar-title
    tooltip(:docs="`Back to the main page`", :show-underline="false")
      v-btn(href="/", text, dark)
        span {{ appTitle }}
  div.px-1
  tooltip(:docs="`API`", :show-underline="false")
    v-btn(:href="apiUrl", target="blank", text, dark)
      span API
  v-spacer
  v-btn(href="https://epigraphdb.org", target="_blank", text, dark)
    img(alt="", src="@/assets/epigraphdb-logo-white.png", height="35px")
  v-sheet(color="transparent")
    .py-2
    a(href="https://mrcieu.github.io", target="_blank")
      img(alt="", src="@/assets/MRC_IEU_Bristol_White.svg", height="59px")
</template>

<script lang="ts">
import Vue from "vue";

import { web_backend_url } from "@/config";

export default Vue.extend({
  name: "AppBar",
  data: () => ({
    appTitle: "TraitHunter",
    apiUrl: web_backend_url,
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
  background-color: rgba(146, 44, 20, 0.8);
  color: white;
  backdrop-filter: blur(5px);
}
</style>
