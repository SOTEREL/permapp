import Vue from "vue";

import MapApi from "@/api/Map";

export default {
  async load({ commit, rootState }) {
    const cfg = await MapApi.load(rootState.project.id);
    commit("setup", cfg.setup);
  },

  async loadBorders({ commit, rootState }) {
    const borders = await MapApi.loadBorders(rootState.project.id);
    commit("setBorders", borders.borders);
  },

  addTiles({ getters, commit }, tiles) {
    const uniqueTiles = tiles.filter(tile => {
      const key = getters.getTileKey(tile);
      return !getters.hasTile(key);
    });
    commit("_addTiles", uniqueTiles);
  },
};
