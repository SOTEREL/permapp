import Vue from "vue";
import Vuex from "vuex";

import MapModule from "./modules/map";
import ProjectModule from "./modules/project";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    map: MapModule,
    project: ProjectModule,
  },
});
