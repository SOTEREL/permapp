function LineStringMapWidget(config) {
  FeatureMapWidget(config, "LineString", {
    edit: true,
    draw: {
      circle: false,
      circlemarker: false,
      marker: false,
      polygon: false,
      polyline: {
        shapeOptions: config.featureStyle || {},
      },
      rectangle: false,
    },
  }).init();
}
