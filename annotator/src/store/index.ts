import Vue from "vue";
import Vuex from "vuex";
import { annotationData, AnnotationDataState } from "./annotationData";
import { io, IoState } from "./io";

Vue.use(Vuex);

export type State = {
  annotationData: AnnotationDataState;
  io: IoState;
};

const store = new Vuex.Store<State>({
  modules: {
    annotationData: annotationData,
    io: io,
  },
});

export default store;
