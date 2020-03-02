function FeatureMapWidget(mapId, field, kwargs) {
  var widget = MapWidget(mapId, field, kwargs);
  var drawnItems = new L.FeatureGroup();

  widget.update = function(data) {
    field.value = JSON.stringify(data);
  };

  function updateFromDrawing() {
    // TODO: circles are points. How to get the radius?
    var geom = drawnItems.toGeoJSON().features[0].geometry;
    widget.update({ geom: geom });
  }

  // TODO:
  // TypeError: points is undefined
  // getPointsCenter http://127.0.0.1:8000/static/api/js/map-tools.js:36
  // _initMapCenter http://127.0.0.1:8000/static/api/js/widgets/map.js:66
  // init http://127.0.0.1:8000/static/api/js/widgets/map.js:78
  // FeatureMapWidget http://127.0.0.1:8000/static/api/js/widgets/feature-map.js:15
  widget.init([MapTools.layers.satellite, drawnItems]);

  widget.map.addControl(
    new L.Control.Draw({
      edit: {
        featureGroup: drawnItems,
        poly: {
          allowIntersection: false,
        },
      },
      draw: {
        polygon: {
          allowIntersection: false,
          showArea: false,
        },
        rectangle: {
          showArea: false,
        },
        circlemarker: false,
      },
    })
  );

  // TODO: draw when editing feature

  widget.map.on(L.Draw.Event.DRAWSTART, function(event) {
    drawnItems.clearLayers();
  });

  widget.map.on(L.Draw.Event.DRAWSTOP, updateFromDrawing);
  widget.map.on(L.Draw.Event.EDITSTOP, updateFromDrawing);

  widget.map.on(L.Draw.Event.CREATED, function(event) {
    var layer = event.layer;
    drawnItems.addLayer(layer);
  });
}
