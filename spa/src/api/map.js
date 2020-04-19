import Vue from "vue";

import ProjectApi from "./project";

const load = (endpoint, pid) => {
  return Vue.axios
    .get(`/map/${endpoint}/`, {
      project: pid,
    })
    .then(resp => resp.data);
};

export default {
  get(pid) {
    return ProjectApi.get(pid).then(data => ({
      lat: data.map_lat,
      lng: data.map_lng,
      zoom: data.map_zoom,
    }));
  },

  getBorders(pid) {
    return Vue.axios.get(`/projects/${pid}/borders/`).then(resp => resp.data);
  },

  listFeatures(pid) {
    return load("features", pid);
  },

  listFeatureTypes(pid) {
    // For now, the types are not project-specific. We keep the pid arg for later.
    return Vue.axios.get("/map/feature_types/").then(resp => resp.data);
  },

  getFeatureDrawing(fid) {
    return Vue.axios
      .get(`/map/features/${fid}/drawing/`)
      .then(resp => resp.data);
  },

  listCategories(pid) {
    // For now, the categories are not project-specific. We keep the pid arg for later.
    return Vue.axios.get("/map/categories/").then(resp => resp.data);
  },
};
