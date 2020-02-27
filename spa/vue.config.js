const path = require("path");

module.exports = {
  lintOnSave: false,
  publicPath: process.env.PUBLIC_PATH,
  outputDir: path.resolve(__dirname, "static/spa/build"),
  indexPath: path.resolve(__dirname, "templates/spa/index.html"),
};
