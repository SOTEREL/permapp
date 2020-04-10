import Vue from "vue";
import Api from "../api";

const plugin = Vue => {
  if (plugin.installed) {
    return;
  }
  plugin.installed = true;

  Vue.$api = Api;

  Object.defineProperties(Vue.prototype, {
    $api: {
      get() {
        return Api;
      },
    },
  });
};

Vue.use(plugin);
