import Vue from "vue";

// Mutations beginning with "_" must be called by an action
export default {
  setupView(state, cfg) {
    state.view = { ...state.view, ...cfg };
  },
  setBorders(state, borders) {
    state.borders = borders;
  },
  _setBackgrounds(state, uniqueBackgrounds) {
    Vue.set(state.view, "backgrounds", uniqueBackgrounds);
  },
};
