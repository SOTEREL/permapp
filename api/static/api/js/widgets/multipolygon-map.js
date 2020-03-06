function MultiPolygonMapWidget(config) {
  FeatureMapWidget(config, "MultiPolygon", {
    edit: true,
    draw: {
      circle: false,
      circlemarker: false,
      marker: false,
      polygon: true,
      polyline: false,
      rectangle: false,
    },
  });
}
