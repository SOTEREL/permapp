import actions from "./actions";
import getters from "./getters";
import mutations from "./mutations";

export default {
  namespaced: true,
  state: {
    setup: {
      zoom: 13,
      lat: 0,
      lng: 0,
    },
    view: {
      backgrounds: ["satellite-geoportal"],
      features: [],
    },
    features: {
      background: {
        "satellite-geoportal": {},
      },
    },
    interaction: null,
  },
  mutations,
  actions,
  getters,
};
