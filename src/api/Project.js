import axios from "axios";

export default {
  list() {
    return axios.get("/data/projects.json").then(resp => resp.data);
  },

  load(pid) {
    return axios.get(`/data/${pid}/config.json`).then(resp => resp.data);
  },
};
