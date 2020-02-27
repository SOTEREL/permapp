import Api from "./api";
import ProjectApi from "./Project";

export default {
  load(pid) {
    return ProjectApi.load(pid).then(data => ({
      lat: data.map_lat,
      lng: data.map_lng,
      zoom: data.map_zoom,
    }));
  },

  loadBorders(pid) {
    return axios.get(`/data/${pid}/borders.json`).then(resp => resp.data);
  },
};
