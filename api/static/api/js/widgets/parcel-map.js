function ParcelMapWidget(mapId, field) {
  var map = L.map(mapId);
  var parcel;

  function readData() {
    return JSON.parse(field.value);
  }

  function updateData(data) {
    field.value = JSON.stringify(data);
    if (parcel) map.removeLayer(parcel);
    // TODO: better style
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
    ).addTo(map);
  }

  map.setView([44.19040294, 2.66266848], 18); // TODO: get from project
  LeafletTools.layers.satellite.addTo(map);
  LeafletTools.layers.cadastral.addTo(map);

  updateData(readData());

  // TODO: cursor pointer
  map.on("click", function(e) {
    // TODO:
    // * Loader
    // * HTTP errors
    LeafletTools.api.parcelFromPos(e.latlng).then(function(parcel) {
      LeafletTools.api.parcelShape(parcel).then(function(geom) {
        parcel.geom = geom;
        updateData(parcel);
      });
    });
  });
}
