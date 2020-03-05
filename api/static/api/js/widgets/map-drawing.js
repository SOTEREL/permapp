function MapDrawingWidget(config, kwargs) {
  var self = {};
  self.mapWidget = null;
  var drawnItems = new L.FeatureGroup();

  self.draw = function(data) {
    throw "MapDrawingWidget.draw() must be implemented";
  };

  self.updateFromDrawing = function() {
    throw "MapDrawingWidget.updateFromDrawing() must be implemented";
  };

  self.drawStart = function(e) {
    drawnItems.eachLayer(function(layer) {
      layer.setOpacity(0.5);
    });
  };

  self.drawStop = self.editStop = function(e) {
    drawnItems.eachLayer(function(layer) {
      layer.setOpacity(1);
    });
    self.updateFromDrawing(drawnItems);
  };

  self.drawCreated = function(e) {
    drawnItems.clearLayers();
    var layer = e.layer;
    drawnItems.addLayer(layer);
  };

  self.init = function(mapWidget, drawControlOptions) {
    self.mapWidget = mapWidget;
    self.mapWidget.map.addLayer(drawnItems);
    var data = self.mapWidget.read();
    if (self.mapWidget.isDataValid(data)) {
      self.draw(data, drawnItems);
    }
    self.mapWidget.map.addControl(new L.Control.Draw(drawControlOptions));

    mapWidget.map.on(L.Draw.Event.DRAWSTART, self.drawStart);
    mapWidget.map.on(L.Draw.Event.DRAWSTOP, self.drawStop);
    mapWidget.map.on(L.Draw.Event.EDITSTOP, self.editStop);
    mapWidget.map.on(L.Draw.Event.CREATED, self.drawCreated);
  };

  return self;
}
