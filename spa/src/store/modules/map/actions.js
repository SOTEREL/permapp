import Vue from "vue";

export default {
  async load({ commit, rootState }) {
    const cfg = await Vue.$api.map.load(rootState.project.id);
    commit("setupView", cfg);
  },

  async loadBorders({ commit, rootState }) {
    const borders = await Vue.$api.map.loadBorders(rootState.project.id);
    commit("setBorders", borders.borders);
  },

  showBackground({ state, commit }, id) {
    const bg = [...state.view.backgrounds, id];
    commit("_setBackgrounds", [...new Set(bg)]);
  },

  hideBackground({ state, commit }, id) {
    let bg = new Set(state.view.backgrounds);
    bg.delete(id);
    commit("_setBackgrounds", [...bg]);
  },

  setBackgrounds({ commit }, bg) {
    commit("_setBackgrounds", [...new Set(bg)]);
  },
};
