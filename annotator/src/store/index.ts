import Vue from "vue";
import Vuex from "vuex";
import { annotationData, AnnotationDataState } from "./annotationData";

Vue.use(Vuex);

export type State = {
  annotationData: AnnotationDataState;
};

const store = new Vuex.Store<State>({
  modules: {
    annotationData: annotationData,
  },
});

export default store;
