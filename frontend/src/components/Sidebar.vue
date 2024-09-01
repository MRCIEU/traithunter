<template lang="pug">
v-card.mt-3.px-3(elevation="12", width="256")
  v-navigation-drawer(floating, permanent)
    h1 TraitHunter
    p API connected: {{ apiConnected }}
    v-divider.py-3
    v-list(dense)
      v-list-item-group(v-model="selectedItem", color="primary")
        v-list-item(v-for="(item, idx) in items", :key="idx", link)
          v-list-item-content
            v-list-item-title {{ item.title }}
</template>

<script lang="ts">
import Vue from "vue";
import { getPing } from "@/funcs/backend-requests";
export default Vue.extend({
  name: "Sidebar",
  data: () => ({
    items: [{ title: "foo" }, { title: "bar" }],
    apiConnected: false,
  }),
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
    selectedItem() {
      return 0;
    },
  },
  mounted: async function () {
    this.apiConnected = await getPing();
  },
});
</script>

<style scoped></style>
