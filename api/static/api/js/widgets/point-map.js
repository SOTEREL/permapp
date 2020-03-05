function PointMapWidget(config, kwargs) {
  var mapWidget = MapWidget(config, kwargs);
  var drawingWidget = MapDrawingWidget(config, kwargs);

  mapWidget.readers = {
    lat: function(field) {
      return parseFloat(field.value);
    },
    lng: function(field) {
      return parseFloat(field.value);
    },
  };

  mapWidget.centerFromData = function(data) {
    return data;
  };

  mapWidget.isDataValid = function(data) {
    return !isNaN(data.lat) && !isNaN(data.lng);
  };

  drawingWidget.draw = function(data, drawingLayer) {
    drawingLayer.clearLayers();
    L.marker(data).addTo(drawingLayer);
  };

  drawingWidget.updateFromDrawing = function(drawingLayer) {
    var feature = drawingLayer.toGeoJSON().features[0];
    if (feature === undefined) {
      return;
    }
    var coords = feature.geometry.coordinates;
    mapWidget.update({
      lat: coords[1],
      lng: coords[0],
    });
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
