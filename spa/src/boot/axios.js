import Vue from "vue";
import axios from "axios";
import VueAxios from "vue-axios";

Vue.use(
  VueAxios,
  axios.create({
    baseURL: process.env.VUE_APP_API_URL,
  })
);
