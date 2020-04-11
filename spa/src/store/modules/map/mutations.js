import Vue from "vue";

// Mutations beginning with "_" must be called by an action
export default {
  setupView(state, cfg) {
    state.view = { ...state.view, ...cfg };
  },

  setBorders(state, data) {
    state.borders = data;
  },

  setFeatures(state, data) {
    state.features = data;
  },

  setFeatureTypes(state, data) {
    state.featureTypes = data;
  },

  setCategories(state, data) {
    state.categories = data;
  },

  addFeatureDrawing(state, { fid, drawing }) {
    Vue.set(state.featureDrawings, fid, drawing);
  },

  showFeatureOnTop(state, fid) {
    if (state.view.features.includes(fid)) {
      return;
    }
    if (!state.features[fid] || !state.features[fid].is_drawable) {
      return;
    }
    Vue.set(state.view, "features", [...state.view.features, fid]);
  },

  hideFeature(state, fid) {
    Vue.set(
      state.view,
      "features",
      state.view.features.filter(x => x !== fid)
    );
  },
};
