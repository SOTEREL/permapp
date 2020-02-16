import axios from 'axios';

export default {
  list() {
    return axios.get('/data/projects.json').then(resp => resp.data)
  },

  loadConfig(id) {
    return axios.get(`/data/${id}/config.json`).then(resp => resp.data)
  },

  loadBorders(id) {
    return axios.get(`/data/${id}/borders.json`).then(resp => resp.data)
  },
}
