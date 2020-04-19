import Vue from "vue";

import { NonDrawableFeatureError } from "@/exceptions";

export default {
  async load({ commit, rootState }) {
    const cfg = await Vue.$api.map.get(rootState.project.id);
    commit("setupView", cfg);
  },

  async loadBorders({ commit, rootState }) {
    const data = await Vue.$api.map.getBorders(rootState.project.id);
    commit("setBorders", data);
  },

  async loadFeatures({ commit, rootState }) {
    const [features, types, categories] = await Promise.all([
      Vue.$api.map.listFeatures(rootState.project.id),
      Vue.$api.map.listFeatureTypes(rootState.project.id),
      Vue.$api.map.listCategories(rootState.project.id),
    ]);
    commit(
      "setFeatures",
      features.reduce((o, feat) => ({ ...o, [feat.id]: feat }), {})
    );
    commit("setFeatureTypes", types);
    commit("setCategories", categories);
  },

  async showFeatureOnTop({ state, commit }, fid) {
    if (!state.features[fid] || !state.features[fid].is_drawable) {
      throw new NonDrawableFeatureError(fid);
    }
    const drawing = await Vue.$api.map.getFeatureDrawing(fid);
    commit("addFeatureDrawing", { fid, drawing });
    commit("showFeatureOnTop", fid);
  },

  toggleFeature({ state, dispatch, commit }, fid) {
    return state.view.features.includes(fid)
      ? commit("hideFeature", fid)
      : dispatch("showFeatureOnTop", fid);
  },
};
