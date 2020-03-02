function ProjectMapWidget(mapId, field) {
  var widget = MapWidget(mapId, field);
  var center;

  widget.update = function(data) {
    if (
      data.map_lat === null ||
      data.map_lng === null ||
      data.map_zoom === null
    ) {
      return;
    }
    field.value = JSON.stringify(data);
    widget.map.setView([data.map_lat, data.map_lng], data.map_zoom);
    if (center) widget.map.removeLayer(center);
    center = L.marker([data.map_lat, data.map_lng]).addTo(widget.map);
  };

  function updateFromPos() {
    var c = widget.map.getCenter();
    data = {
      map_lat: c.lat,
      map_lng: c.lng,
      map_zoom: widget.map.getZoom(),
    };
    widget.update(data);
  }

  var originalData = widget.read();
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
        widget.update(originalData);
      };

      return container;
    },
  });
  widget.map.addControl(new resetControl());

  widget.init([MapTools.layers.satellite]);

  updateFromPos(); // Call it to show marker
  widget.map.on("move", updateFromPos);
  widget.map.on("zoomend", updateFromPos);
}
