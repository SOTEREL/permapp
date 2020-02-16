import axios from 'axios';

export default {
  load(id) {
    return axios.get(`/data/${id}/config.json`).then(resp => resp.data)
  },
  list() {
    return axios.get('/data/projects.json').then(resp => resp.data)
  }
}
