<template lang="pug">
v-app
  app-bar
  v-main
    router-view
    snackbar-widget
</template>


<script lang="ts">
import Vue from "vue";
import AppBar from "@/components/AppBar.vue";
import SnackbarWidget from "@/components/widgets/Snackbar.vue";

import { gtagId } from "@/config";

export default Vue.extend({
  name: "App",
  components: {
    AppBar,
    SnackbarWidget,
  },
  data: () => ({
    //
  }),
});
</script>
