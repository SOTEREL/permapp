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
  load(pid) {
    return ProjectApi.load(pid).then(data => ({
      lat: data.map_lat,
      lng: data.map_lng,
      zoom: data.map_zoom,
    }));
  },

  loadBorders(pid) {
    return load("borders", pid);
  },

  loadFeatures(pid) {
    return load("features", pid);
  },

  loadFeatureTypes(pid) {
    // For now, the types are not project-specific. We keep the pid arg for later.
    return Vue.axios.get("/map/feature_types/").then(resp => resp.data);
  },

  loadFeatureDrawing(fid) {
    return Vue.axios
      .get(`/map/features/${fid}/drawing/`)
      .then(resp => resp.data);
  },

  loadCategories(pid) {
    // For now, the categories are not project-specific. We keep the pid arg for later.
    return Vue.axios.get("/map/categories/").then(resp => resp.data);
  },
};
