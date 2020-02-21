import Vue from "vue";

import ProjectApi from "@/api/Project";

export default {
  namespaced: true,
  state: {
    id: null,
    name: "",
    apiKeys: {
      ign: null,
    },
  },
  mutations: {
    setId(state, id) {
      state.id = id;
    },
    setName(state, name) {
      state.name = name;
    },
    setApiKeys(state, keys) {
      for (let k in keys) {
        Vue.set(state.apiKeys, k, keys[k]);
      }
    },
  },
  actions: {
    async load({ commit }, pid) {
      const cfg = await ProjectApi.load(pid);
      commit("setId", pid);
      commit("setName", cfg.name);
      commit("setApiKeys", cfg.apiKeys);
    },
  },
  getters: {},
};
