import Vue from "vue";

import ProjectApi from "./project";

export default {
  load(pid) {
    return ProjectApi.load(pid).then(data => ({
      lat: data.map_lat,
      lng: data.map_lng,
      zoom: data.map_zoom,
    }));
  },

  loadBorders(pid) {
    return Vue.axios
      .get("/map/borders/", {
        project: pid,
      })
      .then(resp => resp.data);
  },
};
