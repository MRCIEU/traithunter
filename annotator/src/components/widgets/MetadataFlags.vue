<template lang="pug">
div
  v-data-table.elevation-1(:headers="headers", :items="flagItems")
    template(v-slot:top)
      v-toolbar(flat)
        v-toolbar-title Flags / tags
        span.mx-4
        span.font-weight-thin Add/edit flags or initialize a default set of flags
        v-divider.mx-4(inset, vertical)
        v-spacer
        v-dialog(v-model="dialog", max-width="500px")
          template(v-slot:activator="{ on, attrs }")
            v-btn.mb-2(color="primary", dark, v-bind="attrs", v-on="on") New Item
          v-card
            v-card-title
              span.text-h5 {{ formTitle }}
            v-card-text
              v-container
                v-text-field(
                  v-model="editedItem.name",
                  label="Name of the flag"
                )
                br
                v-text-field(
                  v-model="editedItem.desc",
                  label="Short description on the flag"
                )
            v-card-actions
              v-spacer
              v-btn(color="red darken-1", text, @click="close") Cancel
              v-btn(color="blue darken-1", text, @click="save") Save
        v-dialog(v-model="dialogDelete", max-width="500px")
          v-card
            v-card-title.text-h5 Are you sure you want to delete this item?
            v-card-actions
              v-spacer
              v-btn(color="red darken-1", text, @click="closeDelete") Cancel
              v-btn(color="blue darken-1", text, @click="deleteItemConfirm") OK
    template(v-slot:item.actions="{ item }")
      v-icon.mr-2(small, @click="editItem(item)") mdi-pencil
      v-icon.mr-2(small, @click="deleteItem(item)") mdi-delete
    template(v-slot:no-data)
      v-btn(color="warning", @click="initialize") Initialize
</template>

<script lang="ts">
import Vue from "vue";
import * as metadataFlags from "@/resources/metadata-flags";
import * as types from "@/types/types";

export default Vue.extend({
  name: "MetadataFlags",
  components: {
    //
  },
  data: () => ({
    dialog: false,
    dialogDelete: false,
    headers: metadataFlags.headers.concat({
      text: "Actions",
      value: "actions",
      sortable: false,
    }),
    editedIndex: -1,
    editedItem: {
      name: "",
      desc: "",
    },
    defaultItem: {
      name: "",
      desc: "",
    },
    initItems: metadataFlags.initItems,
  }),
  computed: {
    formTitle(): string {
      return this.editedIndex === -1 ? "New Item" : "Edit Item";
    },
    flagItems: {
      get(): Array<types.FlagItem> {
        return this.$store.state.annotationData.metadata.flags;
      },
      async set(newVal): Promise<void> {
        await this.$store.dispatch("annotationData/updateMetadata", {
          prop: "flags",
          value: newVal,
        });
      },
    },
  },
  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },
  methods: {
    initialize() {
      this.flagItems = JSON.parse(JSON.stringify(this.initItems));
    },
    editItem(item) {
      this.editedIndex = this.flagItems.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item) {
      this.editedIndex = this.flagItems.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },
    deleteItemConfirm() {
      this.flagItems.splice(this.editedIndex, 1);
      this.closeDelete();
    },
    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.flagItems[this.editedIndex], this.editedItem);
      } else {
        this.flagItems.push(this.editedItem);
      }
      this.close();
    },
  },
});
</script>
