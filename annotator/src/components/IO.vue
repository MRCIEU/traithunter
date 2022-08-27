<template lang="pug">
v-container
  v-row
    v-col(cols="6")
      v-btn(@click="specifyInput", :disabled="inputDone") Specify Input file
      | &nbsp; Input file: {{ inputName }}
  div
  v-row
    v-col(cols="6")
      v-btn(@click="specifyOutput", :disabled="outputDone") Specify output file
      | &nbsp; Output file: {{ outputName }}
    v-col(cols="4")
      span Progress saved at: {{ lastSaveTime }}
</template>

<script lang="ts">
import Vue from "vue";
import * as io from "@/funcs/io";
import * as types from "@/types/types";
import * as processing from "@/funcs/processing";

export default Vue.extend({
  name: "IO",
  components: {
    //
  },
  data() {
    return {
      inputDone: false,
      outputDone: false,
      inputData: null,
    };
  },
  computed: {
    inputInfo: {
      get(): File {
        return this.$store.state.io.input;
      },
      async set(info: File) {
        await this.$store.dispatch("io/updateInput", info);
      },
    },
    outputInfo: {
      get(): File {
        return this.$store.state.io.output;
      },
      async set(info: File) {
        await this.$store.dispatch("io/updateOutput", info);
      },
    },
    inputName(): string {
      return this.inputInfo != null ? this.inputInfo.name : "Unspecified";
    },
    outputName(): string {
      return this.outputInfo != null ? this.outputInfo.name : "Unspecified";
    },
    lastSaveTime(): string {
      return this.$store.state.io.saveTime;
    },
  },
  watch: {
    async inputData(newVal) {
      if (newVal) {
        this.$store.commit("annotationData/transformInputData", this.inputData);
      }
    },
  },
  methods: {
    async specifyInput(): Promise<any> {
      const fileInfo = await io.getInputFile();
      console.log(fileInfo);
      console.log(fileInfo.name);
      this.inputInfo = fileInfo;
      let reader = new FileReader();
      reader.readAsText(fileInfo);
      reader.onload = () => {
        this.inputData = JSON.parse(reader.result as string) as types.InputData;
        this.inputDone = true;
      };
    },
    async specifyOutput(): Promise<any> {
      const fileInfo = await io.getOutputFile();
      this.outputInfo = fileInfo;
      this.outputDone = true;
      console.log(fileInfo);
      console.log(fileInfo.name);
    },
  },
});
</script>
