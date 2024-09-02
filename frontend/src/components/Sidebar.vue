<template lang="pug">
v-card.mt-3.px-3(elevation="12", max-width="256")
  v-navigation-drawer(floating, permanent)
    v-list(dense, three-line)
      v-list-item-group(v-model="selectedItem", color="primary")
        v-list-item(
          v-for="(item, idx) in items",
          :key="idx",
          :href="item.path",
          link
        )
          v-list-item-content
            v-list-item-title {{ item.title }}
            v-list-item-subtitle {{ item.desc }}
    v-divider.py-3
    p API connected: {{ apiConnected }}
</template>

<script lang="ts">
import Vue from "vue";
import { getPing } from "@/funcs/backend-requests";
import { pathOutline } from "@/resources/resources";

export default Vue.extend({
  name: "Sidebar",
  data: () => ({
    items: pathOutline,
    apiConnected: false,
  }),
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
    selectedItem() {
      const res = this._.chain(this.items)
        .findIndex((e) => e.name == this.currentRouteName)
        .value();
      return res;
    },
  },
  mounted: async function () {
    this.apiConnected = await getPing();
  },
});
</script>

<style scoped></style>
