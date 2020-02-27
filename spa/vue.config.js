const path = require("path");

module.exports = {
  lintOnSave: false,
  publicPath: "/static/spa/build/",
  outputDir: path.resolve(__dirname, "static/spa/build"),
  indexPath: path.resolve(__dirname, "templates/spa/index.html"),
};
