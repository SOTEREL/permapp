export const NonDrawableFeatureError = function(fid, message) {
  this.name = "NonDrawableFeatureError";
  this.message = message || `The feature ${fid} is not drawable.`;
};
