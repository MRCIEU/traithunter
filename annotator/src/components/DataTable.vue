<template lang="pug">
v-container(fluid)
  div(v-if="dataItems != null")
    v-data-iterator(
      :items="dataItems",
      item-key="trait_id",
      :items-per-page="5",
      :search="search"
    )
      template(v-slot:header)
        v-toolbar.mb-1(dark, color="teal lighten-1")
          v-row
            v-spacer
            v-col(cols="8")
              v-text-field(
                v-model="search",
                clearable,
                flat,
                solo-inverted,
                hide-details,
                label="Search query term"
              )
            v-spacer
      template(v-slot:default="props")
        div(v-for="item in props.items", :key="item.trait_id")
          item-display(
            :idx="item.idx",
            :trait-id="item.trait_id",
            :trait-term="item.trait_term"
          )
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
      search: null,
    };
  },
  computed: {
    //
  },
  mounted() {
    this.dataItems = this._.chain(this.$store.state.annotationData.data)
      .map((e) => ({ trait_id: e.trait_id, trait_term: e.trait_term }))
      .map((e, idx) => ({ idx: idx, ...e }))
      .value();
  },
  methods: {
    //
  },
});
</script>
