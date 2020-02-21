import Vue from "vue";

import MapApi from "@/api/Map";

export default {
  namespaced: true,
  state: {
    setup: {
      zoom: 13,
      lat: 0,
      lng: 0,
    },
    view: {
      tiles: ["satellite"],
      features: [],
    },
    interaction: null,
  },
  mutations: {
    setInitialZoom(state, zoom) {
      Vue.set(state.setup, "zoom", zoom);
    },
    setInitialCenter(state, { lat, lng }) {
      Vue.set(state.setup, "lat", lat);
      Vue.set(state.setup, "lng", lng);
    },
    setBorders(state, borders) {
      state.borders = borders;
    },
  },
  actions: {
    async load({ commit, rootState }) {
      const cfg = await MapApi.load(rootState.project.id);
      commit("setInitialZoom", cfg.setup.zoom);
      commit("setInitialCenter", {
        lat: cfg.setup.lat,
        lng: cfg.setup.lng,
      });
    },
    async loadBorders({ commit, rootState }) {
      const borders = await MapApi.loadBorders(rootState.project.id);
      commit("setBorders", borders.borders);
    },
  },
  getters: {},
};
