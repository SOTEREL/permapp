function MapWidget(mapId, field, subfields, kwargs) {
  var self = {};
  kwargs = kwargs || {};

  var _projectField = document.getElementById(kwargs.project_field_id);
  var _loading = false;
  var _formRow = django.jQuery("#" + mapId).closest(".form-row");
  var _errorUl = django.jQuery('<ul class="errorlist"></ul>');

  self.map = L.map(mapId);

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

  self.read = function() {
    var data = {};
    for (var name in subfields) {
      data[name] = document.getElementById(subfields[name]).value;
    }
    return data;
  };

  self.update = function(data) {
    throw "Not implemented";
  };

  function _setMapCenterFromProject() {
    if (_projectField) {
      var projectId = _projectField.value;
      if (projectId === "") {
        return;
      }
      fetch("/_api/projects/" + projectId + "/") // TODO: store url in var
        .then(function(resp) {
          return resp.json();
        })
        .then(function(project) {
          self.map.setView(
            [project.map_lat, project.map_lng],
            project.map_zoom
          );
        })
        .catch(self.error);
    }
  }

  function _initMapCenter() {
    var geom = self.read().geom;
    if (geom) {
      var center = MapTools.geo.getPointsCenter(geom.coordinates[0][0]);
      self.map.setView([center.lat, center.lng], 18);
    } else if (!_setMapCenterFromProject()) {
      self.map.setView(
        kwargs.defaultView || [46.55886030311719, 2.0654296875000004],
        kwargs.defaultZoom || 5
      );
    }
  }

  self.init = function(layers) {
    _formRow.prepend(_errorUl);
    _initMapCenter();
    for (var layer of layers) {
      layer.addTo(self.map);
    }
    self.update(self.read());
    self.loading(false);
  };

  if (_projectField) {
    _projectField.addEventListener("change", _setMapCenterFromProject);
  }

  return self;
}
