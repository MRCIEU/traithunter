import * as types from "@/types/types";
import * as processing from "@/funcs/processing";

import { ActionContext } from "vuex";
import { State } from ".";

export type AnnotationDataState = {
  data: types.AnnotationData | null;
  metadata: types.AnnotationMetadata;
};

type Context = ActionContext<AnnotationDataState, State>;

type ItemPropPayload = {
  id: string;
  prop: string;
  value: any;
};

type MetadataPayload = {
  prop: string;
  value: any;
};

export const annotationData = {
  namespaced: true,
  state: (): AnnotationDataState => ({
    data: null,
    metadata: {
      flags: [],
    },
  }),
  getters: {
    annotationDataExport(
      state: AnnotationDataState,
    ): types.AnnotationDataExport {
      const res = {
        metadata: state.metadata,
        data: state.data,
      };
      return res;
    },
  },
  mutations: {
    async transformInputData(
      state: AnnotationDataState,
      {
        inputData,
        inputType,
      }: {
        inputData: types.InputData;
        inputType: string;
      },
    ): Promise<void> {
      state.data = await processing.transformInputData(inputData);
    },
    async updateItemProp(
      state: AnnotationDataState,
      payload: ItemPropPayload,
    ): Promise<void> {
      state.data[payload.id][payload.prop] = payload.value;
    },
    async updateMetadata(
      state: AnnotationDataState,
      payload: MetadataPayload,
    ): Promise<void> {
      state.metadata[payload.prop] = payload.value;
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
    async updateMetadata(
      context: Context,
      payload: MetadataPayload,
    ): Promise<void> {
      context.commit("updateMetadata", payload);
    },
  },
};
