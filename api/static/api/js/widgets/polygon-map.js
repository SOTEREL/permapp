function PolygonMapWidget(config) {
  FeatureMapWidget(config, "Polygon", {
    edit: true,
    draw: {
      circle: false,
      circlemarker: false,
      marker: false,
      polygon: {
        shapeOptions: config.featureStyle || {},
      },
      polyline: false,
      rectangle: true,
    },
  }).init();
}
