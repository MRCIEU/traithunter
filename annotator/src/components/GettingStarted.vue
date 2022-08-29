<template lang="pug">
div
  p
    span First specify the input file and its filetype, &nbsp;
    | then specify the output file to save. &nbsp;
    | For detailed documentation please consult the &nbsp;
    a(href="/docs", target="_blank") Documentation
    | &nbsp; page.
  p
    span Remeber to save your progress regularly.
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "GettingStarted",
  components: {
    //
  },
  data() {
    return {
      //
    };
  },
  computed: {
    //
  },
  methods: {
    //
  },
});
</script>
