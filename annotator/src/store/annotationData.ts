import * as types from "@/types/types";
import * as processing from "@/funcs/processing";

import { ActionContext } from "vuex";
import { State } from ".";

export type AnnotationDataState = {
  data: types.AnnotationData | null;
};

type Context = ActionContext<AnnotationDataState, State>;
type CandidatePayload = { id: string; selection: Array<string> };

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
    async updateCandidateSelect(
      state: AnnotationDataState,
      payload: CandidatePayload,
    ): Promise<void> {
      state.data[payload.id]["selection"] = payload.selection;
    },
  },
  actions: {
    async transformInputData(
      context: Context,
      inputData: types.InputData,
    ): Promise<void> {
      context.commit("transformInputData", inputData);
    },
    async updateCandidateSelect(
      context: Context,
      payload: CandidatePayload,
    ): Promise<void> {
      context.commit("updateCandidateSelect", payload);
    },
  },
};
