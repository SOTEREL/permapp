import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import api from "./boot/api";
import axios from "./boot/axios";
import fish from "./boot/fish";

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount("#app");
