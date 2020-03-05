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

  var GeocoderControl = L.Control.extend({
    options: {
      position: "topleft",
    },
    onAdd: function(map) {
      var container = L.DomUtil.create("div", "leaflet-control");
      container.style.display = "flex";

      var icon = L.DomUtil.create("div", "leaflet-bar", container);
      icon.style.background =
        "url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAnFBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4jUzeAAAAM3RSTlMAAQIDBwgJDg8RExcdICMzPUJERUdMUVJcX2F5e36FiZigoqWrtcPF2eDi5Obp6+/z+fuRCq6wAAAAiklEQVQYGVXBRwKCMABFwU8QFbtgwV6wV/Dd/26GZKMzspIbUC5r8swB79mWs4VVHEbDN8+arC6MVWm8Wcpac5Q3pDSSLqTyImhJKujLC6Ej6UQmL4ampBkPI2fFXVb9Q25kjWGkSgKPrJ8egamc5IPzgomcaH4urpuuyWGqX8EeBvoV7FjoT9AzXxZnEVySl7A0AAAAAElFTkSuQmCC) white no-repeat center";
      icon.style.border = "1px solid #000";
      icon.style.width = "30px";
      icon.style.height = "30px";
      icon.style.cursor = "pointer";
      icon.title = "Rechercher un lieu";

      var searchContainer = L.DomUtil.create("div", "", container);
      searchContainer.style.marginLeft = "5px";
      searchContainer.style.display = "none";

      var input = L.DomUtil.create("input", "leaflet-bar", searchContainer);
      input.style.height = "30px";
      input.style.boxSizing = "border-box";
      input.style.margin = "0px";
      input.style.textAlign = "center";

      var results = L.DomUtil.create("div", "leaflet-bar", searchContainer);
      results.style.display = "none";
      results.style.padding = "5px";
      results.style.marginTop = "5px";
      results.style.background = "white";
      results.style.maxHeight = "200px";
      results.style.overflow = "auto";

      function clear() {
        input.value = "";
        results.style.display = "none";
        searchContainer.style.display = "none";
      }

      icon.addEventListener("click", function() {
        if (searchContainer.style.display == "none") {
          searchContainer.style.display = "block";
        } else {
          clear();
        }
      });

      input.addEventListener("keypress", function(e) {
        if (e.keyCode != 13) {
          return;
        }

        e.preventDefault();

        var query = this.value;
        MapTools.geo.geocode(query).then(function(locations) {
          results.innerHTML = "";
          for (var loc of locations) {
            (function(loc) {
              var result = L.DomUtil.create("div", "", results);
              result.innerText =
                loc.placeAttributes.municipality +
                " (" +
                loc.placeAttributes.postalCode +
                ")";
              result.style.cursor = "pointer";

              result.addEventListener("click", function() {
                widget.update({
                  map_lat: loc.position.x,
                  map_lng: loc.position.y,
                  map_zoom: 18,
                });
                clear();
              });
            })(loc);
          }
          if (!locations.length) {
            results.innerHTML = "Aucun résultat";
          }
          results.style.display = "block";
        });
      });

      return container;
    },
  });

  widget.map.addControl(new ResetControl());
  widget.map.addControl(new GeocoderControl());
}
