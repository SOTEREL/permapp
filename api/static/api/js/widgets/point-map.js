function PointMapWidget(config) {
  FeatureMapWidget(config, "Point", {
    edit: false,
    draw: {
      circle: false,
      circlemarker: false,
      marker: true,
      polygon: false,
      polyline: false,
      rectangle: false,
    },
  }).init();
}
