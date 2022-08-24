<template lang="pug">
v-container
  IO
  .py-5
</template>

<script lang="ts">
import Vue from "vue";
import IO from "@/components/IO.vue";

export default Vue.extend({
  name: "Home",
  components: {
    IO,
  },
  data() {
    return {};
  },
  computed: {
    //
  },
  methods: {},
});
</script>
