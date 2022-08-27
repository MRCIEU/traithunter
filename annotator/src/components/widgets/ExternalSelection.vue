<template lang="pug">
div
  v-data-table.elevation-1(:headers="headers", :items="selectionItems")
    template(v-slot:top)
      v-toolbar(flat)
        v-toolbar-title External picks
        v-divider.mx-4(inset, vertical)
        v-spacer
        v-dialog(v-model="dialog", max-width="500px")
          template(v-slot:activator="{ on, attrs }")
            v-btn.mb-2(color="primary", dark, v-bind="attrs", v-on="on", small) New Item
          v-card
            v-card-title
              span.text-h5 {{ formTitle }}
            v-card-text
              v-container
                v-text-field(
                  v-model="editedItem.ent_id",
                  label="Identifier for the ontology item"
                )
                br
                v-text-field(
                  v-model="editedItem.ent_term",
                  label="Term label for the ontology item"
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
</template>

<script lang="ts">
import Vue from "vue";
import * as types from "@/types/types";

// typescript really hates this file, no solutions
export default Vue.extend({
  name: "ExternalSelection",
  components: {
    //
  },
  props: {
    traitId: {
      type: String,
      default: null,
      required: true,
    },
  },
  data() {
    return {
      dialog: false,
      dialogDelete: false,
      headers: [
        {
          text: "ID",
          value: "ent_id",
          align: "start",
        },
        {
          text: "Term label",
          value: "ent_term",
        },
        {
          text: "Actions",
          value: "actions",
          sortable: false,
        },
      ],
      editedIndex: -1,
      editedItem: {
        ent_id: "",
        ent_term: "",
      },
      defaultItem: {
        ent_id: "",
        ent_term: "",
      },
    };
  },
  computed: {
    formTitle(): string {
      return (this.editedIndex as number) === -1 ? "New Item" : "Edit Item";
    },
    selectionItems: {
      get(): Array<types.BaseEnt> {
        const res =
          this.$store.state.annotationData.data[this.traitId]
            .external_selection;
        return res as Array<types.BaseEnt>;
      },
      async set(newVal: any): Promise<void> {
        await this.$store.dispatch("annotationData/updateItemProp", {
          id: this.traitId,
          prop: "external_selection",
          value: newVal,
        });
      },
    },
  },
  watch: {
    dialog(val): void {
      val || this.close();
    },
    dialogDelete(val): void {
      val || this.closeDelete();
    },
  },
  methods: {
    editItem(item): void {
      this.editedIndex = this.selectionItems.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    deleteItem(item): void {
      this.editedIndex = this.selectionItems.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },
    deleteItemConfirm(): void {
      this.selectionItems.splice(this.editedIndex, 1);
      this.closeDelete();
    },
    close(): void {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    closeDelete(): void {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },
    save(): void {
      if (this.editedIndex > -1) {
        Object.assign(this.selectionItems[this.editedIndex], this.editedItem);
      } else {
        this.selectionItems.push(this.editedItem);
      }
      this.close();
    },
  },
});
</script>
