import Vue from "vue";

export default {
  list() {
    return Vue.axios.get("/projects/").then(resp => resp.data);
  },

  get(pid) {
    return Vue.axios.get(`/projects/${pid}/`).then(resp => resp.data);
  },
};
