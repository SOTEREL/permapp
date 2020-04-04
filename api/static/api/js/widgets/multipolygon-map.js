function MultiPolygonMapWidget(config) {
  var w = FeatureMapWidget(config, "MultiPolygon", {
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
  });

  w.drawingWidget.isSingleFeature = false;

  w.drawingWidget.updateFromDrawing = function(drawingLayer) {
    var features = drawingLayer.toGeoJSON().features;
    var coords = [];
    if (features.length) {
      coords = features.map(function(feat) {
        return feat.geometry.coordinates;
      });
    }
    w.mapWidget.update({
      coordinates: coords,
    });
  };

  w.drawingWidget.draw = function(data) {
    for (var coords of data.coordinates) {
      L.geoJSON(
        {
          type: "Feature",
          geometry: {
            type: "Polygon",
            coordinates: coords,
          },
        },
        {
          style: data.path_options,
        }
      ).eachLayer(function(layer) {
        w.drawingWidget.drawnItems.addLayer(layer);
      });
    }
    w.drawingWidget.drawnItems.addTo(w.mapWidget.map);
  };

  w.init();
}
