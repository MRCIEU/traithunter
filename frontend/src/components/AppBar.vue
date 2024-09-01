<template lang="pug">
v-app-bar(id="navbar" app dense flat)
  v-toolbar-title
    tooltip(:docs="`Back to the main page`" :show-underline="false")
      v-btn(href="/" text dark)
        span(class="ml-3")  {{ appTitle }}
  span(class="px-1")
  v-spacer
  v-btn(href="https://epigraphdb.org" target="_blank" text dark)
    img(alt="" src="@/assets/epigraphdb-logo-white.png" height="35px")
  v-sheet(color="transparent")
    div(class="py-2")
    a(href="https://mrcieu.github.io" target="_blank")
      img(alt="" src="@/assets/MRC_IEU_Bristol_White.svg" height="59px")
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  name: "AppBar",
  data: () => ({
    appTitle: "TraitHunter",
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
