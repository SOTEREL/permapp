import axios from "axios";

export default {
  load(pid) {
    return axios.get(`/data/${pid}/map.json`).then(resp => resp.data);
  }
};
