import Api from "./api";

export default {
  list() {
    return Api.get("/projects/").then(resp => resp.data);
  },

  load(pid) {
    return Api.get(`/projects/${pid}/`).then(resp => resp.data);
  },
};
