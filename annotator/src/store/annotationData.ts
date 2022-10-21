import _ from "lodash";

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

type ItemFlagsPayload = {
  traitId: string;
  entId: string;
  value: Array<string>;
}

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
    async flatDataExport(
      state: AnnotationDataState,
    ): Promise<types.FlatExportData> {
      const res = await processing.transformFlatExportData(state.data);
      return res;
    },
    async annotationDataArray(
      state: AnnotationDataState,
    ): Promise<types.AnnotationDataItem> {
      const res = await _.chain(state.data).values().value();
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
      const transformRes = await processing.transformInputData({
        inputData: inputData,
        inputType: inputType,
      });
      if (inputType == "mapping-results") {
        state.data = transformRes.data;
      } else if (inputType == "annotation-results") {
        state.data = transformRes.data;
        state.metadata = transformRes.metadata;
      }
    },
    async updateItemProp(
      state: AnnotationDataState,
      payload: ItemPropPayload,
    ): Promise<void> {
      state.data[payload.id][payload.prop] = payload.value;
    },
    async updateItemCandFlags(
      state: AnnotationDataState,
      payload: ItemFlagsPayload,
    ): Promise<void> {
      state.data[payload.traitId]["cand_flags"] = payload.value;
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
    async updateItemCandFlags(
      context: Context,
      payload: ItemFlagsPayload,
    ): Promise<void> {
      context.commit("updateItemCandFlags", payload);
    },
    async updateMetadata(
      context: Context,
      payload: MetadataPayload,
    ): Promise<void> {
      context.commit("updateMetadata", payload);
    },
  },
};
