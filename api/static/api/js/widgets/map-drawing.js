function MapDrawingWidget(config, kwargs) {
  var self = {};
  self.mapWidget = null;
  var drawnItems = new L.FeatureGroup();

  self.draw = function(data) {
    throw "Not implementedaaaa";
  };

  self.updateFromDrawing = function() {
    throw "Not implementedsssss";
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
    self.draw(self.mapWidget.read(), drawnItems);
    self.mapWidget.map.addControl(new L.Control.Draw(drawControlOptions));

    // TODO: draw when editing feature

    mapWidget.map.on(L.Draw.Event.DRAWSTART, self.drawStart);
    mapWidget.map.on(L.Draw.Event.DRAWSTOP, self.drawStop);
    mapWidget.map.on(L.Draw.Event.EDITSTOP, self.editStop);
    mapWidget.map.on(L.Draw.Event.CREATED, self.drawCreated);
  };

  return self;
}
