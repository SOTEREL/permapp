function PolygonMapWidget(config) {
  FeatureMapWidget(config, "Polygon", {
    edit: true,
    draw: {
      circle: false,
      circlemarker: false,
      marker: false,
      polygon: {
        shapeOptions: config.featureStyle || {},
        showArea: true,
        showLength: true,
        guidelineDistance: 15,
        allowIntersection: false,
      },
      polyline: false,
      rectangle: {
        shapeOptions: config.featureStyle || {},
        showArea: true,
        showLength: true,
        guidelineDistance: 15,
      },
    },
  }).init();
}
