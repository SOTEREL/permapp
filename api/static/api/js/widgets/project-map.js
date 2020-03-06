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

  widget.isDataValid = function(data) {
    return data.map_lat !== "" && data.map_lng !== "" && data.map_zoom !== "";
  };

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

  widget.init([MapTools.layers.satellite]);

  // If the center is not specified in data (probably because we are creating
  // a new project), we use the default center;
  if (!widget.isDataValid(widget.read())) {
    widget.update(readPos());
  }
  widget.map.on("move", updateFromPos);
  widget.map.on("zoomend", updateFromPos);

  var originalData = widget.read();
  var ResetControl = L.Control.extend({
    options: {
      position: "topleft",
    },
    onAdd: function(map) {
      var container = L.DomUtil.create("div", "leaflet-bar leaflet-control");
      container.style.background =
        "url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAh1BMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD3YishAAAALHRSTlMAAgQGCA0SFB4fICcoKistNERKVnR+f46PoKKqq7e5xcjP09re5Ovt8fP7/eIYXwAAAABsSURBVBhXjY03FoIAAMUCKihWxF5B7OT+53NQcPOZ6SfLh3+JOgTjwdenPiexNj4zTd00IVjfh4v56FGH9rFMdrrtlbYA4ss+OakW3cM5AvLl8Kaq1/4qB0IqP1SEAKhmmTYv7/krFHUo+IcXJhsO/oWZbWkAAAAASUVORK5CYII=) white no-repeat center";
      container.style.border = "1px solid #000";
      container.style.width = "30px";
      container.style.height = "30px";
      container.style.cursor = "pointer";
      container.title = "Revenir au départ";

      container.addEventListener("click", function() {
        widget.update(originalData);
      });

      return container;
    },
  });

  widget.map.addControl(new ResetControl());
  widget.map.addControl(
    new MapTools.controls.GeocoderControl({
      onSelectLocation: function(loc) {
        widget.update({
          map_lat: loc.position.x,
          map_lng: loc.position.y,
          map_zoom: 18,
        });
      },
    })
  );
}
