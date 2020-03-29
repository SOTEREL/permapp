function MapWidget(config) {
  var self = {};

  var _projectField = document.getElementById(config.project_field_id);
  var _loading = false;
  var _formRow = django.jQuery("#" + config.mapId).closest(".form-row");
  var _errorUl = django.jQuery('<ul class="errorlist"></ul>');

  self.map = L.map(config.mapId);

  self.loading = function(val) {
    if (val === undefined) {
      return _loading;
    }
    _loading = val;
    if (_loading) {
      self.map.getContainer().style.opacity = 0.1;
      self.map.getContainer().style.cursor = "progress";
    } else {
      self.map.getContainer().style.opacity = 1;
      self.map.getContainer().style.cursor = "pointer";
    }
  };

  self.error = function(err) {
    _errorUl.html("<li>" + err + "</li>");
  };

  self.apiError = function(err) {
    self.error(err);
    self.loading(false);
  };

  self.readers = {
    coordinates: function(field) {
      return JSON.parse(field.value);
    },
    path_options: function(field) {
      return JSON.parse(field.value);
    },
  };
  self.writers = {
    coordinates: function(field, value) {
      field.value = JSON.stringify(value);
    },
    path_options: function(field, value) {
      field.value = JSON.stringify(value);
    },
    map_projection: function(field, value) {
      field.value = self.map.options.crs.code;
    },
  };

  self.read = function() {
    var data = {};
    for (var name in config.subfields) {
      if (self.readers[name]) {
        data[name] = self.readers[name](
          document.getElementById(config.subfields[name])
        );
      } else {
        data[name] = document.getElementById(config.subfields[name]).value;
      }
    }
    return data;
  };

  self.isDataValid = function(data) {
    throw "MapWidget.isDataValid() must be implemented";
  };

  self.update = function(data) {
    if (!self.isDataValid(data)) {
      return;
    }
    for (var name in config.subfields) {
      if (self.writers[name]) {
        self.writers[name](
          document.getElementById(config.subfields[name]),
          data[name]
        );
      } else {
        document.getElementById(config.subfields[name]).value = data[name];
      }
    }
    config.mapField.value = JSON.stringify(data);
    self.postUpdate(data);
  };

  self.postUpdate = function(data) {};

  self.centerFromData = function(data) {};

  function _setMapCenterFromProject() {
    var projectId = _projectField.value;
    if (projectId === "") {
      return;
    }
    fetch("/_api/projects/" + projectId + "/") // TODO: store url in var
      .then(function(resp) {
        return resp.json();
      })
      .then(function(project) {
        self.map.setView([project.map_lat, project.map_lng], project.map_zoom);
      })
      .catch(self.error);
  }

  function _initMapCenter() {
    var isDataValid = self.isDataValid(self.read());
    var dataCenter = !isDataValid
      ? config.mapCenter
      : self.centerFromData(self.read());
    if (dataCenter !== undefined) {
      return self.map.setView(
        [dataCenter.lat, dataCenter.lng],
        dataCenter.zoom || 18
      );
    }
    if (_projectField && _projectField.value !== "") {
      return _setMapCenterFromProject();
    }
    self.map.setView(
      config.defaultView || [46.55886030311719, 2.0654296875000004],
      config.defaultZoom || 5
    );
  }

  self.init = function(defaultLayerName, baseLayers, overlays) {
    _formRow.prepend(_errorUl);
    _initMapCenter();
    baseLayers[defaultLayerName].addTo(self.map);
    L.control
      .layers(baseLayers, overlays, {
        hideSingleBase: true,
        position: "topleft",
      })
      .addTo(self.map);
    self.update(self.read());
    self.loading(false);
  };

  if (_projectField) {
    _projectField.addEventListener("change", _setMapCenterFromProject);
  }

  return self;
}
