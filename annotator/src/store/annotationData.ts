import * as types from "@/types/types";
import * as processing from "@/funcs/processing";

import { ActionContext } from "vuex";
import { State } from ".";

export type AnnotationDataState = {
  data: types.AnnotationData | null;
};

type Context = ActionContext<AnnotationDataState, State>;

export const annotationData = {
  namespaced: true,
  state: (): AnnotationDataState => ({
    data: null,
  }),
  getters: {
    //
  },
  mutations: {
    async transformInputData(
      state: AnnotationDataState,
      inputData: types.InputData,
    ): Promise<void> {
      state.data = await processing.transformInputData(inputData);
    },
  },
  actions: {
    async transformInputData(
      context: Context,
      inputData: types.InputData,
    ): Promise<void> {
      context.commit("transformInputData", inputData);
    },
  },
};
