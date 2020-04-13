export default {
  getCategoryById: state => id => {
    return state.categories.find(cat => cat.id === id);
  },

  getCategoryTypes: (state, getters) => cid => {
    const category = getters.getCategoryById(cid);
    return category ? category.feature_types : [];
  },

  getTypeFeatures: (state, getters) => (tid, drawableOnly = false) => {
    const features = Object.values(state.features).filter(
      feat => feat.type === tid
    );
    return !drawableOnly ? features : features.filter(feat => feat.is_drawable);
  },

  getCategoryFeatures: (state, getters) => (cid, drawableOnly) => {
    const types = getters.getCategoryTypes(cid);
    return types
      .map(type => getters.getTypeFeatures(type.id, drawableOnly))
      .reduce((acc, features) => [...acc, ...features], []);
  },
};
