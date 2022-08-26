import * as types from "@/types/types";
import * as processing from "@/funcs/processing";

import { ActionContext } from "vuex";
import { State } from ".";

export type AnnotationDataState = {
  data: types.AnnotationData | null;
};

type Context = ActionContext<AnnotationDataState, State>;
type ItemPropPayload = {
  id: string;
  prop: string;
  value: any;
};

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
    async updateItemProp(
      state: AnnotationDataState,
      payload: ItemPropPayload,
    ): Promise<void> {
      state.data[payload.id][payload.prop] = payload.value;
    },
  },
  actions: {
    async transformInputData(
      context: Context,
      inputData: types.InputData,
    ): Promise<void> {
      context.commit("transformInputData", inputData);
    },
    async updateItemProp(
      context: Context,
      payload: ItemPropPayload,
    ): Promise<void> {
      context.commit("updateItemProp", payload);
    },
  },
};
