function ProjectMapWidget(mapId, field) {
  var map = L.map(mapId);
  var center;

  function readData() {
    var data = JSON.parse(field.value);
    return {
      lat: data.map_lat,
      lng: data.map_lng,
      zoom: data.map_zoom,
    };
  }

  function updateData(data) {
    if (
      data.lat === undefined ||
      data.lng === undefined ||
      data.zoom === undefined
    ) {
      data = map.getCenter();
      data.zoom = map.getZoom();
    } else {
      map.setView([data.lat, data.lng], data.zoom);
    }
    field.value = JSON.stringify({
      map_lat: data.lat,
      map_lng: data.lng,
      map_zoom: data.zoom,
    });
    if (center) map.removeLayer(center);
    center = L.marker([data.lat, data.lng]).addTo(map);
  }

  var originalData = readData();
  updateData(readData());

  LeafletTools.geoportal
    .SatelliteLayer("ORTHOIMAGERY.ORTHOPHOTOS", "normal", "image/jpeg")
    .addTo(map);

  map.on("move", updateData);
  map.on("zoomend", updateData);

  var resetControl = L.Control.extend({
    options: {
      position: "topleft",
    },
    onAdd: function(map) {
      var container = L.DomUtil.create(
        "div",
        "leaflet-bar leaflet-control leaflet-control-custom"
      );
      container.style.background =
        "url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAA4ElEQVQYGQXBsUpCAQAF0PN6L02isjJcg6AhqKXNhoYamxr6HOlrWloigkBEknBxCBxrcApRxLEhGm7nAHDuQUT0XSsAgIaRiIiImGoBUDcXny7UFWrOjMWvfYAn8agEUHkX8aWAQzFTAagMxcyHuISuuAVQGYq5LafiFSaiBSi9ibltrIso+BENUBqIhR1ARMVEtFHqi6UmoBJRcC/ulHpiqQngRPThSKz0xMouAIbiCngRsbIHgK6YKoANCzHVUUPp2ED8OQBg01hERER8awMAdDyLiJEbawAAQKFSAAD/Jphh2xjysk4AAAAASUVORK5CYII=) white no-repeat center";
      container.style.border = "1px solid #000";
      container.style.width = "30px";
      container.style.height = "30px";
      container.style.cursor = "pointer";
      container.title = "Revenir au départ";

      container.onclick = function() {
        updateData(originalData);
      };

      return container;
    },
  });
  map.addControl(new resetControl());
}
