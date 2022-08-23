<template lang="pug">
v-container
  v-btn(@click="specifyInput") Specify Input file
  v-btn(@click="specifyOutput") Specify output file
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
    async specifyInput(): Promise<any> {
      const fileInfo = await this.getInputFile();
      console.log(fileInfo);
      console.log(fileInfo.name);
      let reader = new FileReader();
      reader.readAsText(fileInfo);
      reader.onload = () => {
        this.fileContent = JSON.parse(reader.result as string);
      };
    },
    async specifyOutput(): Promise<any> {
      const fileInfo = await this.getOutputFile();
      console.log(fileInfo);
      console.log(fileInfo.name);
      const writableStream = await fileInfo.createWritable();
      await writableStream.write(this.foobar);
      await writableStream.close();
    },
    async getInputFile(): Promise<any> {
      const pickerOpts = {
        types: [
          {
            description: "JSON file",
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
    async getOutputFile(): Promise<any> {
      const pickerOpts = {
        suggestedName: "annotation_results.json",
        types: [
          {
            description: "JSON file",
            accept: {
              "application/*": [".json"],
            },
          },
        ],
      };
      return await window.showSaveFilePicker(pickerOpts);
    },
  },
});
</script>
