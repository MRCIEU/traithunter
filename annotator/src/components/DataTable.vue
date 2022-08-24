<template lang="pug">
v-container
  div(v-if="dataItems != null")
    v-data-iterator(
      :items="dataItems",
      item-key="trait_id",
      :items-per-page="10"
    )
      template(v-slot:default="props")
        div(v-for="item in props.items" :key="item.ent_id")
          span {{ item.trait_term }}
          v-divider
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "DataTable",
  components: {
    //
  },
  data() {
    return {
      dataItems: [],
    };
  },
  computed: {
    //
  },
  mounted() {
    this.dataItems = this._.chain(this.$store.state.annotationData.data)
      .map((v, k) => (v))
      .value();
  },
  methods: {
    //
  },
});
</script>
