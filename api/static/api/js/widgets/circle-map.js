function CircleMapWidget(config) {
  var w = FeatureMapWidget(config, "Point", {
    edit: true,
    draw: {
      circle: {
        shapeOptions: config.featureStyle || {},
        showRadius: true,
      },
      circlemarker: false,
      marker: false,
      polygon: false,
      polyline: false,
      rectangle: false,
    },
  });

  w.mapWidget.readers.radius = function(field) {
    return parseFloat(field.value);
  };

  w.drawingWidget.updateFromDrawing = function(drawingLayer) {
    var circle = drawingLayer.getLayers()[0];
    if (circle === undefined) {
      return;
    }
    var center = circle.getLatLng();
    w.mapWidget.update({
      coordinates: [center.lng, center.lat],
      radius: circle.getRadius(),
    });
  };

  w.drawingWidget.draw = function(data) {
    var lat = data.coordinates[1];
    var lng = data.coordinates[0];
    var options = config.featureStyle || {};
    options.radius = data.radius;
    w.drawingWidget.drawnItems.addLayer(
      L.circle({ lat: lat, lng: lng }, options)
    );
    w.drawingWidget.drawnItems.addTo(w.mapWidget.map);
  };

  w.init();
}
