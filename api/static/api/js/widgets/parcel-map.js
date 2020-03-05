function ParcelMapWidget(config, kwargs) {
  var widget = MapWidget(config, kwargs);
  var parcel;

  widget.isDataValid = function(data) {
    return (
      data.insee !== "" &&
      data.section !== "" &&
      data.number !== "" &&
      data.geom !== "null"
    );
  };

  widget.centerFromData = function(data) {
    if (!data.coordinates) return;
    return MapTools.geo.center.fromMultiPolygon(data.coordinates);
  };

  widget.readers = {
    coordinates: function(field) {
      return JSON.parse(field.value);
    },
  };

  widget.writers = {
    coordinates: function(field, value) {
      field.value = JSON.stringify(value);
    },
  };

  widget.postUpdate = function(data) {
    if (parcel) {
      widget.map.removeLayer(parcel);
    }
    parcel = L.geoJSON(
      {
        type: "Feature",
        geometry: {
          type: "MultiPolygon",
          coordinates: data.coordinates,
        },
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
            parcel.coordinates = geom.coordinates;
            widget.update(parcel);
          })
          .catch(widget.apiError);
      })
      .catch(widget.apiError);
  });

  widget.init([MapTools.layers.satellite, MapTools.layers.cadastral]);
}
