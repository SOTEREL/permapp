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

  self.styleOptions = null;

  self.getPathOptions = function(layer) {
    var feature = layer.getLayers()[0];
    if (feature === undefined) {
      return {};
    } else if (feature instanceof L.Marker) {
      return {
        icon: feature.options.icon.options,
      };
    }
    var options = feature.options;
    if (feature instanceof L.Circle) {
      options.radius = feature.getRadius();
    }
    return options;
  };

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
        style: data.path_options,
        pointToLayer: function(geoJsonPoint, latlng) {
          var options = django.jQuery.extend(true, {}, data.path_options);
          if (options.icon !== undefined) {
            options.icon = L.icon(options.icon);
          }
          return L.marker(latlng, options);
        },
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
    self.mapWidget.update({
      coordinates: coords,
      path_options: self.getPathOptions(drawingLayer),
    });
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

  self.styleChanged = function(element) {
    self.updateFromDrawing(self.drawnItems);
  };

  self.drawCreated = function(e) {
    if (self.isSingleFeature) {
      self.drawnItems.clearLayers();
    }
    var layer = e.layer;
    self.drawnItems.addLayer(layer);
  };

  self.init = function(drawCtrlOpts, styleCtrlOpts) {
    self.mapWidget.map.addLayer(self.drawnItems);

    var data = self.mapWidget.read();
    if (self.mapWidget.isDataValid(data)) {
      self.draw(data);
    }

    styleCtrlOpts = styleCtrlOpts || {};
    if (styleCtrlOpts.openOnLeafletDraw === undefined) {
      styleCtrlOpts.openOnLeafletDraw = true;
    }
    if (styleCtrlOpts.showTooltip === undefined) {
      styleCtrlOpts.showTooltip = false;
    }
    if (styleCtrlOpts.forms === undefined) {
      styleCtrlOpts.forms = {
        geometry: {
          color: L.StyleEditor.formElements.ColorElement,
          opacity: L.StyleEditor.formElements.OpacityElement,
          weight: L.StyleEditor.formElements.WeightElement,
          dashArray: L.StyleEditor.formElements.DashElement,
          fillColor: L.StyleEditor.formElements.ColorElement,
          fillOpacity: L.StyleEditor.formElements.OpacityElement,
          popupContent: false, // We already have a description field
        },
        marker: {
          icon: L.StyleEditor.formElements.IconElement,
          color: L.StyleEditor.formElements.ColorElement,
          size: L.StyleEditor.formElements.SizeElement,
        },
      };
    }
    self.styleOptions = styleCtrlOpts.forms;
    self.mapWidget.map.addControl(L.control.styleEditor(styleCtrlOpts));

    if (drawCtrlOpts.edit === true) {
      drawCtrlOpts.edit = {
        featureGroup: self.drawnItems,
      };
    } else if (drawCtrlOpts.edit) {
      drawCtrlOpts.edit.featureGroup = self.drawnItems;
    }
    self.mapWidget.map.addControl(new L.Control.Draw(drawCtrlOpts));

    self.mapWidget.map.on(L.Draw.Event.DRAWSTART, self.drawStart);
    self.mapWidget.map.on(L.Draw.Event.DRAWSTOP, self.drawStop);
    self.mapWidget.map.on(L.Draw.Event.EDITSTOP, self.editStop);
    self.mapWidget.map.on(L.Draw.Event.DELETESTOP, self.deleteStop);
    self.mapWidget.map.on(L.Draw.Event.CREATED, self.drawCreated);
    self.mapWidget.map.on("styleeditor:changed", self.styleChanged);
  };

  return self;
}
