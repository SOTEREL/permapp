function ParcelMapWidget(mapId, field, kwargs) {
  var widget = MapWidget(mapId, field, kwargs);
  var parcel;

  widget.update = function(data) {
    field.value = JSON.stringify(data);
    if (parcel) widget.map.removeLayer(parcel);
    parcel = L.geoJSON(
      {
        type: "Feature",
        geometry: data.geom,
        properties: {
          insee: data.insee,
          section: data.section,
          number: data.number,
        },
      },
      {
        style: {
          fillColor: "white",
          fillOpacity: 0.5,
          color: "#000",
          weight: 1,
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

  widget.map.on("click", function(e) {
    if (widget.loading()) {
      return;
    }
    widget.loading(true);
    MapTools.geo
      .parcelFromPos(e.latlng)
      .then(function(parcel) {
        MapTools.geo
          .parcelShape(parcel)
          .then(function(geom) {
            parcel.geom = geom;
            widget.update(parcel);
          })
          .catch(widget.apiError);
      })
      .catch(widget.apiError);
  });

  widget.init([MapTools.layers.satellite, MapTools.layers.cadastral]);
}
