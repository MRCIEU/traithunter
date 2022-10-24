<template lang="pug">
div
  span Flags for this candidate
  v-combobox(
    v-model="flagSelect",
    :items="flagItems",
    chips,
    clearable,
    label="flags",
    multiple,
    preprend-icon="mdi-filter-variant",
  )
    template(v-slot:selection="{ attrs, item, select, selected }")
      v-chip(
        v-bind="attrs",
        :input-value="selected",
        close,
        @click="select",
        @click:close="flagRemove(item)"
      )
        span {{ item }} &nbsp;
</template>

<script lang="ts">
import Vue from "vue";
import { PropType } from "vue";
import * as types from "@/types/types";

export default Vue.extend({
  name: "CandFlags",
  components: {
    //
  },
  props: {
    entId: {
      type: String,
      required: true,
    },
    traitId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      //
    };
  },
  computed: {
    flagItems(): Array<string> {
      const flags = this.$store.state.annotationData.metadata.flags;
      const res = this._.chain(flags)
        .map((e) => e.name)
        .value() as Array<string>;
      return res;
    },
    flagSelect: {
      get(): Array<string> {
        const flags =
          this.$store.state.annotationData.data[this.traitId].cand_flags[
            this.entId
          ];
        return flags as Array<string>;
      },
      async set(newVal: Array<string>) {
        const flags = this._.chain(newVal)
          .filter((e) => this.flagItems.includes(e))
          .value();
        await this.$store.dispatch("annotationData/updateItemCandFlags", {
          traitId: this.traitId,
          entId: this.entId,
          value: flags,
        });
      },
    },
  },
  methods: {
    flagRemove(item) {
      (this as any).flagSelect.splice(
        (this as any).flagSelect.indexOf(item),
        1,
      );
    },
  },
});
</script>
