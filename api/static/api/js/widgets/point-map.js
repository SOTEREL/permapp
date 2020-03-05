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

  drawingWidget.draw = function(data, drawingLayer) {
    if (isNaN(data.lat) || isNaN(data.lng)) {
      return;
    }
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

  // TODO:
  // TypeError: points is undefined
  // getPointsCenter http://127.0.0.1:8000/static/api/js/map-tools.js:36
  // _initMapCenter http://127.0.0.1:8000/static/api/js/widgets/map.js:66
  // init http://127.0.0.1:8000/static/api/js/widgets/map.js:78
  // FeatureMapWidget http://127.0.0.1:8000/static/api/js/widgets/feature-map.js:15
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
