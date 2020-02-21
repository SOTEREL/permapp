import Vue from "vue";

import MapApi from "@/api/Map";

export default {
  namespaced: true,
  state: {
    setup: {
      zoom: 13,
      lat: 0,
      lng: 0
    },
    borders: []
  },
  mutations: {
    setInitialZoom(state, zoom) {
      Vue.set(state.setup, "zoom", zoom);
    },
    setInitialCenter(state, { lat, lng }) {
      Vue.set(state.setup, "lat", lat);
      Vue.set(state.setup, "lng", lng);
    }
  },
  actions: {
    async load({ commit }, pid) {
      const cfg = await MapApi.load(pid);
      commit("setInitialZoom", cfg.setup.zoom);
      commit("setInitialCenter", {
        lat: cfg.setup.lat,
        lng: cfg.setup.lng
      });
    }
  },
  getters: {}
};
