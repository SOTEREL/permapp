function CircleMapWidget(config) {
  // TODO: style
  FeatureMapWidget(config, "Point", {
    edit: true,
    draw: {
      circle: true,
      circlemarker: false,
      marker: false,
      polygon: false,
      polyline: false,
      rectangle: false,
    },
  }).init();
}
