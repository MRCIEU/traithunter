<template lang="pug">
v-app
  app-bar
  v-main
    router-view
</template>

<script lang="ts">
import Vue from "vue";
import AppBar from "@/components/AppBar.vue";

export default Vue.extend({
  name: "App",
  components: {
    AppBar,
  },
  data: () => ({
    //
  }),
});
</script>

<style lang="scss"></style>
