<template lang="pug">
v-btn(@click="populateContent") Load data
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  name: "Home",
  components: {
    //
  },
  data() {
    return {
      fileContent: null,
      foobar: "foo--bar",
    };
  },
  computed: {
    //
  },
  methods: {
    async populateContent(): Promise<any> {
      const fileInfo = await this.getFile();
      let reader = new FileReader();
      reader.readAsText(fileInfo);
      reader.onload = () => {
        this.fileContent = JSON.parse(reader.result as string);
      };
    },
    async getFile(): Promise<any> {
      const pickerOpts = {
        types: [
          {
            description: "result file",
            accept: {
              "application/*": [".json"],
            },
            excludeAcceptAllOption: true,
            multiple: false,
          },
        ],
      };
      var fileHandle;
      [fileHandle] = await window.showOpenFilePicker(pickerOpts);
      const fileInfo = await fileHandle.getFile();
      return fileInfo;
    },
  },
});
</script>
