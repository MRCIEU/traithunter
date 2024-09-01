<template lang="pug">
v-card.mt-3.px-3(elevation="12", width="256")
  v-navigation-drawer(floating, permanent)
    h1 TraitHunter
    p API connected: {{ apiConnected }}
    v-divider.py-3
    v-list(dense)
      v-list-item-group(v-model="selectedItem", color="primary")
        v-list-item(v-for="(item, idx) in items", :key="idx", :href="item.path", link)
          v-list-item-content
            v-list-item-title {{ item.title }}
</template>

<script lang="ts">
import Vue from "vue";
import { getPing } from "@/funcs/backend-requests";
export default Vue.extend({
  name: "Sidebar",
  data: () => ({
    items: [
      { title: "About", name: "About", path: "/about" },
      { title: "Trait mapping", name: "Home", path: "/" },
      { title: "Pairwise similarity", name: "Pairwise", path: "/pairwise" },
    ],
    apiConnected: false,
  }),
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
    selectedItem() {
      const res = this._.chain(this.items).findIndex((e) => (e.name == this.currentRouteName)).value();
      return res;
    },
  },
  mounted: async function () {
    this.apiConnected = await getPing();
  },
});
</script>

<style scoped></style>
