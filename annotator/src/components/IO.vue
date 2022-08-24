<template lang="pug">
v-container
  v-btn(@click="specifyInput", :disabled="inputDone") Specify Input file
  | &nbsp; Input file: {{ inputName }}
  div
  v-btn(@click="specifyOutput", :disabled="outputDone") Specify output file
  | &nbsp; Output file: {{ outputName }}
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
      inputInfo: null,
      outputInfo: null,
      inputDone: false,
      outputDone: false,
      inputData: null,
    };
  },
  computed: {
    inputName(): string {
      return this.inputInfo != null ? this.inputInfo.name : "Unspecified";
    },
    outputName(): string {
      return this.outputInfo != null ? this.outputInfo.name : "Unspecified";
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
