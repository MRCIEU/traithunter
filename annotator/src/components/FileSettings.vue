<template lang="pug">
v-container
  v-stepper(v-model="stage", vertical, v-if="!initDone")
    v-stepper-step(:complete="stage > 1", step="1") Configure input
    v-stepper-content(step="1")
      div
        v-btn(@click="specifyInput") Specify Input file
        | &nbsp; Input file: {{ inputName }}
        .py-5
        span Specify input type
        v-radio-group(v-model="inputType", row)
          v-radio(
            v-for="(item, idx) in _.chain(inputTypeOptions).values().value()",
            :key="idx",
            :label="item.label",
            :value="item.value"
          )
      v-btn(color="primary", @click="finishStage1", :disabled="!inputDone") Continue
    v-stepper-step(:complete="stage > 2", step="2") Configure output
    v-stepper-content(step="2")
      div
        v-btn(@click="specifyOutput", :disabled="outputDone") Specify output file
        | &nbsp; Output file: {{ outputName }}
      .py-5
      v-btn(
        color="primary",
        @click="finishStage2",
        :disabled="!outputDone || initDone"
      ) Initialize session
  div(v-if="initDone")
    h2 Input settings
    p Input file: {{ inputName }}
    p Input type: {{ inputTypeOptions[inputType].label }}
    h2 Output settings
    p Output file: {{ outputName }}
    p Save status: {{ saveStatus }}
</template>

<script lang="ts">
import Vue from "vue";
import * as io from "@/funcs/io";
import * as types from "@/types/types";
import * as processing from "@/funcs/processing";

export default Vue.extend({
  name: "FileSettings",
  components: {
    //
  },
  data() {
    return {
      stage: 1,
      inputData: null,
      inputType: null,
      inputTypeOptions: {
        "mapping-results": {
          label: "Mapping results",
          value: "mapping-results",
        },
        "annotation-results": {
          label: "Annotation results",
          value: "annotation-results",
        },
      },
    };
  },
  computed: {
    inputDone(): boolean {
      const res = Boolean(this.inputInfo != null && this.inputType != null);
      return res;
    },
    outputDone(): boolean {
      const res = this.outputInfo != null;
      return res;
    },
    initDone: {
      get(): boolean {
        return this.$store.state.io.initDone;
      },
      async set(val: boolean) {
        if (val) {
          await this.$store.commit("io/initDone");
        }
      },
    },
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
    saveStatus(): string {
      const saveTime = this.$store.state.io.saveTime;
      if (!saveTime) {
        return "Progress has not been saved";
      } else {
        return `Last saved at ${saveTime}`;
      }
    },
  },
  methods: {
    async finishStage1() {
      this.stage = 2;
    },
    async finishStage2(): Promise<void> {
      await this.$store.commit("annotationData/transformInputData", {
        inputData: this.inputData,
        inputType: this.inputType,
      });
      this.initDone = true;
      this.stage = 3;
    },
    async specifyInput(): Promise<any> {
      const fileInfo = await io.getInputFile();
      console.log(fileInfo);
      console.log(fileInfo.name);
      this.inputInfo = fileInfo;
      let reader = new FileReader();
      reader.readAsText(this.inputInfo);
      reader.onload = () => {
        this.inputData = JSON.parse(reader.result as string) as types.InputData;
      };
    },
    async specifyOutput(): Promise<any> {
      const fileInfo = await io.getOutputFile();
      this.outputInfo = fileInfo;
    },
  },
});
</script>
