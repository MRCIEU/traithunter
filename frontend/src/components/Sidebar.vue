<template lang="pug">
v-card(elevation="12" width="256" class="mt-3 px-3")
  v-navigation-drawer(floating, permanent)
    h1 TraitHunter
    v-divider(class="py-3")
    v-list(dense)
      v-list-item-group(v-model="selectedItem", color="primary")
        v-list-item(v-for="(item, idx) in items", :key="idx", link)
          v-list-item-content
            v-list-item-title {{ item.title }}
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  name: "Sidebar",
  data: () => ({
    items: [
      {"title": "foo"},
      {"title": "bar"},
    ]
  }),
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
    selectedItem() {
      return 0;
    }
  },
});
</script>

<style scoped>
</style>
