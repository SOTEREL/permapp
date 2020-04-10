import Vue from "vue";

export default {
  namespaced: true,
  state: {
    id: null,
    name: "",
    apiKeys: {
      geoportal: process.env.VUE_APP_GEOPORTAL_API_KEY,
    },
  },
  mutations: {
    setId(state, id) {
      state.id = id;
    },
    setName(state, name) {
      state.name = name;
    },
  },
  actions: {
    async load({ commit }, pid) {
      const cfg = await Vue.$api.project.load(pid);
      commit("setId", pid);
      commit("setName", cfg.name);
    },
  },
  getters: {},
};
