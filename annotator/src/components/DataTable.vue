<template lang="pug">
v-container
  div(v-if="dataItems != null")
    v-data-iterator(
      :items="dataItems",
      item-key="trait_id",
      :items-per-page="10"
    )
      template(v-slot:default="props")
        div(v-for="item in props.items", :key="item.trait_id")
          item-display(:trait-id="item.trait_id")
          v-divider
          .py-2
</template>

<script lang="ts">
import Vue from "vue";
import ItemDisplay from "@/components/widgets/ItemDisplay.vue";

export default Vue.extend({
  name: "DataTable",
  components: {
    ItemDisplay,
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
      .keys()
      .map((e) => ({ trait_id: e }))
      .value();
  },
  methods: {
    //
  },
});
</script>
