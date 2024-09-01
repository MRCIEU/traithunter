<template lang="pug">
v-app
  app-bar
  v-main
    router-view
    snackbar-widget
  app-footer
</template>


<script lang="ts">
import Vue from "vue";
import AppBar from "@/components/AppBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import SnackbarWidget from "@/components/widgets/Snackbar.vue";
import CookieConsent from "vue-cookieconsent-component";

import { gtagId } from "@/config";

export default Vue.extend({
  name: "App",
  components: {
    AppBar,
    AppFooter,
    SnackbarWidget,
    CookieConsent,
  },
  data: () => ({
    //
  }),
});
</script>
