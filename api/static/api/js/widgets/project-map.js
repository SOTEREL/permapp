function ProjectMapWidget(config) {
  var widget = MapWidget(config);
  var center;

  function readPos() {
    var c = widget.map.getCenter();
    return {
      map_lat: c.lat,
      map_lng: c.lng,
      map_zoom: widget.map.getZoom(),
    };
  }

  widget.postUpdate = function(data) {
    widget.map.setView([data.map_lat, data.map_lng], data.map_zoom);
    if (center) {
      widget.map.removeLayer(center);
    }
    center = L.marker([data.map_lat, data.map_lng]).addTo(widget.map);
  };

  function updateFromPos(e) {
    // Triggered by map.setView()
    if (e.type === "move" && e.originalEvent === undefined) {
      return;
    }
    widget.update(readPos());
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

  // If the center is not specified in data (probably because we are creating
  // a new project), we use the default center;
  if (!widget.isDataValid(widget.read())) {
    widget.postUpdate(readPos());
  }
  widget.map.on("move", updateFromPos);
  widget.map.on("zoomend", updateFromPos);
}
