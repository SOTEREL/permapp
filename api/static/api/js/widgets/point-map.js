function PointMapWidget(config, kwargs) {
  var mapWidget = MapWidget(config, kwargs);
  var drawingWidget = MapDrawingWidget(config, kwargs);

  mapWidget.centerFromData = function(data) {
    return {
      lng: data.coordinates[0],
      lat: data.coordinates[1],
    };
  };

  mapWidget.isDataValid = function(data) {
    return (
      data.coordinates &&
      !isNaN(data.coordinates[0]) &&
      !isNaN(data.coordinates[1])
    );
  };

  drawingWidget.draw = function(data, drawingLayer) {
    drawingLayer.clearLayers();
    L.marker({
      lng: data.coordinates[0],
      lat: data.coordinates[1],
    }).addTo(drawingLayer);
  };

  drawingWidget.updateFromDrawing = function(drawingLayer) {
    var feature = drawingLayer.toGeoJSON().features[0];
    if (feature === undefined) {
      return;
    }
    var coords = feature.geometry.coordinates;
    mapWidget.update({ coordinates: coords });
  };

  mapWidget.init([MapTools.layers.satellite]);

  drawingWidget.init(mapWidget, {
    edit: false,
    draw: {
      circle: false,
      circlemarker: false,
      polygon: false,
      polyline: false,
      rectangle: false,
    },
  });
}
