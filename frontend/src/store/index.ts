import Vue from "vue";
import Vuex from "vuex";

import { snackbar, snackbarState } from "./snackbar";

Vue.use(Vuex);

export type State = {
  snackbar: snackbarState;
};

const store = new Vuex.Store<State>({
  modules: {
    snackbar: snackbar,
  },
});

export default store;
