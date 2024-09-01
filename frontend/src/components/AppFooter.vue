<template lang="pug">
v-footer(:id="footer" padless fixed)
  p Footer
</template>

<script lang="ts">
import Vue from "vue";
export default Vue.extend({
  name: "AppFooter",
  data: () => ({
    //
  }),
  computed: {
    //
  },
  mounted: function () {
    //
  },
  methods: {
    //
  },
});
</script>

<style scoped>
#footer {
  background-color: rgba(21, 62, 62, 0.8);
  color: white;
  backdrop-filter: blur(5px);
}
</style>
