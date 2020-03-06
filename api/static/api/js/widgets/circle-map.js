function CircleMapWidget(config) {
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
  });
}
