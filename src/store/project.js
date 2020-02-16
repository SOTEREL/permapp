import Vue from "vue";

import ProjectApi from '@/api/Project';

export default {
  namespaced: true,
  state: {
    id: null,
    name: '',
    apiKeys: {
      ign: null
    },
    map: {
      zoom: 13,
      lat: 0,
      lng: 0,
    },
  },
  mutations: {
    setId (state, id) {
      state.id = id;
    },
    setName (state, name) {
      state.name = name;
    },
    setApiKeys (state, keys) {
      for (let k in keys) {
        Vue.set(state.apiKeys, k, keys[k]);
      }
    },
    setMapZoom (state, zoom) {
      Vue.set(state.map, 'zoom', zoom);
    },
    setMapCenter (state, { lat, lng} ) {
      Vue.set(state.map, 'lat', lat);
      Vue.set(state.map, 'lng', lng);
    },
  },
  actions: {
    async load ({ commit, state }, pid) {
      const cfg = await ProjectApi.loadConfig(pid);
      commit('setId', pid);
      commit('setName', cfg.name);
      commit('setApiKeys', cfg.apiKeys);
      commit('setMapZoom', cfg.map.zoom);
      commit('setMapCenter', {
        lat: cfg.map.lat,
        lng: cfg.map.lng
      });
    }
  },
  getters: {}
};
