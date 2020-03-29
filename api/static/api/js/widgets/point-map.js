function PointMapWidget(config) {
  FeatureMapWidget(config, "Point", {
    edit: false,
    draw: {
      circle: false,
      circlemarker: false,
      marker: {
        icon:
          config.featureStyle !== null
            ? L.icon(config.featureStyle)
            : new L.Icon.Default(),
      },
      polygon: false,
      polyline: false,
      rectangle: false,
    },
  }).init();
}
