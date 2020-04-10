import actions from "./actions";
import getters from "./getters";
import mutations from "./mutations";

export const getInitialState = () => {
  return {
    view: {
      zoom: 13,
      lat: 0,
      lng: 0,
      features: null,
    },
    features: null,
  };
};

export default {
  namespaced: true,
  state: getInitialState(),
  mutations,
  actions,
  getters,
};
