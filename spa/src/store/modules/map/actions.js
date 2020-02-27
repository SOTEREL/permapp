import Vue from "vue";

import MapApi from "@/api/Map";

export default {
  async load({ commit, rootState }) {
    const cfg = await MapApi.load(rootState.project.id);
    commit("setup", cfg);
  },

  async loadBorders({ commit, rootState }) {
    const borders = await MapApi.loadBorders(rootState.project.id);
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
