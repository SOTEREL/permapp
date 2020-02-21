import axios from "axios";

export default {
  load(pid) {
    return axios.get(`/data/${pid}/map.json`).then(resp => resp.data);
  },

  loadBorders(pid) {
    return axios.get(`/data/${pid}/borders.json`).then(resp => resp.data);
  },
};
