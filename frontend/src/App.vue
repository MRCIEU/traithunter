<template lang="pug">
v-app
  app-bar
  v-main
    v-row
      v-col(cols="2")
        sidebar
      v-col
        router-view
    snackbar-widget
</template>

<script lang="ts">
import Vue from "vue";
import AppBar from "@/components/AppBar.vue";
import Sidebar from "@/components/Sidebar.vue";
import SnackbarWidget from "@/components/widgets/Snackbar.vue";

export default Vue.extend({
  name: "App",
  components: {
    AppBar,
    Sidebar,
    SnackbarWidget,
  },
  data: () => ({
    //
  }),
});
</script>
