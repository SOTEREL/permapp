function MapDrawingWidget(config, mapWidget) {
  var self = {};
  self.mapWidget = mapWidget;
  self.drawnItems = new L.FeatureGroup();

  self.mapWidget.centerFromData = function(data) {
    return MapTools.geo.center["from" + config.geomType](data.coordinates);
  };

  self.mapWidget.isDataValid = function(data) {
    return data.coordinates; // TODO
  };

  self.isSingleFeature = true;

  self.draw = function(data) {
    if (!data.coordinates || !config.geomType) {
      throw "Unknown geometry type, MapDrawingWidget.draw() must be implemented";
    }
    self.drawnItems = L.geoJSON(
      {
        type: "Feature",
        geometry: {
          type: config.geomType,
          coordinates: data.coordinates,
        },
      },
      {
        style: {}, // TODO
      }
    );
    self.drawnItems.addTo(self.mapWidget.map);
  };

  self.updateFromDrawing = function(drawingLayer) {
    var feature = drawingLayer.toGeoJSON().features[0];
    if (feature === undefined) {
      return;
    }
    var coords = feature.geometry.coordinates;
    self.mapWidget.update({ coordinates: coords });
  };

  self.drawStart = function(e) {
    self.drawnItems.eachLayer(function(layer) {
      try {
        layer.setOpacity(0.5);
      } catch {
        layer.setStyle({
          fillOpacity: 0.5,
          opacity: 0.5,
        });
      }
    });
  };

  self.drawStop = self.editStop = self.deleteStop = function(e) {
    self.drawnItems.eachLayer(function(layer) {
      try {
        layer.setOpacity(1);
      } catch {
        layer.setStyle({
          fillOpacity: 1,
          opacity: 1,
        });
      }
    });
    self.updateFromDrawing(self.drawnItems);
  };

  self.drawCreated = function(e) {
    if (self.isSingleFeature) {
      self.drawnItems.clearLayers();
    }
    var layer = e.layer;
    self.drawnItems.addLayer(layer);
  };

  self.init = function(drawControlOptions) {
    self.mapWidget.map.addLayer(self.drawnItems);

    var data = self.mapWidget.read();
    if (self.mapWidget.isDataValid(data)) {
      self.draw(data);
    }

    if (drawControlOptions.edit === true) {
      drawControlOptions.edit = {
        featureGroup: self.drawnItems,
      };
    } else if (drawControlOptions.edit) {
      drawControlOptions.edit.featureGroup = self.drawnItems;
    }
    self.mapWidget.map.addControl(new L.Control.Draw(drawControlOptions));

    self.mapWidget.map.on(L.Draw.Event.DRAWSTART, self.drawStart);
    self.mapWidget.map.on(L.Draw.Event.DRAWSTOP, self.drawStop);
    self.mapWidget.map.on(L.Draw.Event.EDITSTOP, self.editStop);
    self.mapWidget.map.on(L.Draw.Event.DELETESTOP, self.deleteStop);
    self.mapWidget.map.on(L.Draw.Event.CREATED, self.drawCreated);
  };

  return self;
}
