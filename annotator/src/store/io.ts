import * as types from "@/types/types";

import { ActionContext } from "vuex";
import { State } from ".";

type FileHandle = any;

export type IoState = {
  input: File;
  output: FileHandle;
  initDone: boolean;
  saveTime: string | null;
};

type Context = ActionContext<IoState, State>;

export const io = {
  namespaced: true,
  state: (): IoState => ({
    input: null,
    output: null,
    initDone: false,
    saveTime: null,
  }),
  getters: {
    //
  },
  mutations: {
    async updateInput(state: IoState, info: File): Promise<void> {
      state.input = info;
    },
    async updateOutput(state: IoState, info: File): Promise<void> {
      state.output = info;
    },
    async updateSaveTime(state: IoState, time: string): Promise<void> {
      state.saveTime = time;
    },
    async initDone(state: IoState): Promise<void> {
      state.initDone = true;
    },
  },
  actions: {
    async updateInput(context: Context, info: File): Promise<void> {
      context.commit("updateInput", info);
    },
    async updateOutput(context: Context, info: File): Promise<void> {
      context.commit("updateOutput", info);
    },
    async updateSaveTime(context: Context, time: string): Promise<void> {
      context.commit("updateSaveTime", time);
    },
    async initDone(context: Context): Promise<void> {
      context.commit("initDone");
    },
  },
};
