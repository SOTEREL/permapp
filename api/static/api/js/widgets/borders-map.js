function BordersMapWidget(config, kwargs) {
  var widget = MapWidget(config, kwargs);
  var borders;

  widget.isDataValid = function(data) {
    return true;
  };

  widget.centerFromData = function(data) {
    if (!data.coordinates) return;
    return MapTools.geo.center.fromMultiPolygon(data.coordinates);
  };

  widget.postUpdate = function(data) {
    if (borders) {
      widget.map.removeLayer(borders);
    }
    parcel = L.geoJSON(
      {
        type: "Feature",
        geometry: {
          type: "MultiPolygon",
          coordinates: data.coordinates,
        },
      },
      {
        style: {
          fillOpacity: 0,
          color: "red",
          weight: 2,
        },
        onEachFeature: function(feature, layer) {
          var html = "";
          for (var k in feature.properties) {
            html +=
              "<div><strong>" +
              k +
              ":</strong> " +
              feature.properties[k] +
              "</div>";
          }
          layer.bindPopup(html);
        },
      }
    ).addTo(widget.map);
    widget.loading(false);
  };

  widget.init(
    "Satellite",
    {
      Satellite: MapTools.layers.satellite(),
      IGN: MapTools.layers.ign(),
    },
    {
      Cadastre: MapTools.layers.cadastral(),
    }
  );
}
