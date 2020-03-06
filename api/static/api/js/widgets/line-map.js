function LineMapWidget(config) {
  FeatureMapWidget(config, "LineString", {
    //edit: true,
    draw: {
      circle: false,
      circlemarker: false,
      marker: false,
      polygon: false,
      polyline: true,
      rectangle: false,
    },
  });
}
