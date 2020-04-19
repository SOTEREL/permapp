import Vue from "vue";

export default {
  namespaced: true,
  state: {
    list: null,
    id: null,
    name: "",
  },
  mutations: {
    setList(state, list) {
      state.list = list;
    },
    setLoaded(state, project) {
      state.id = project.id;
      state.name = project.name;
    },
  },
  actions: {
    async list({ commit }) {
      const data = await Vue.$api.project.list();
      commit("setList", data);
    },
    async load({ commit }, pid) {
      const data = await Vue.$api.project.get(pid);
      commit("setLoaded", data);
    },
  },
  getters: {},
};
