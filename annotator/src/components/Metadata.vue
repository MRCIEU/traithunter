<template lang="pug">
v-container
  metadata-flags
</template>

<script lang="ts">
import Vue from "vue";
import MetadataFlags from "@/components/widgets/MetadataFlags.vue";

export default Vue.extend({
  name: "Metadata",
  components: {
    MetadataFlags,
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
