function PolygonMapWidget(config) {
  FeatureMapWidget(config, "Polygon", {
    edit: true,
    draw: {
      circle: false,
      circlemarker: false,
      marker: false,
      polygon: true,
      polyline: false,
      rectangle: true,
    },
  }).init();
}
