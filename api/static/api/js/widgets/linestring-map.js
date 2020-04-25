function LineStringMapWidget(config) {
  var w = FeatureMapWidget(config, "LineString", {
    edit: true,
    draw: {
      circle: false,
      circlemarker: false,
      marker: false,
      polygon: false,
      polyline: {
        shapeOptions: config.featureStyle || {},
        showLength: true,
        guidelineDistance: 15,
      },
      rectangle: false,
    },
  });
  w.init();

  var FreeDrawControl = L.Control.extend({
    options: {
      position: "topleft",
    },
    onAdd: function(map) {
      var active = false;
      var container = L.DomUtil.create("div", "leaflet-control");

      var icon = L.DomUtil.create("div", "leaflet-bar", container);
      icon.style.background =
        "url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAnFBMVEUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD4jUzeAAAAM3RSTlMAAQIDBwgJDg8RExcdICMzPUJERUdMUVJcX2F5e36FiZigoqWrtcPF2eDi5Obp6+/z+fuRCq6wAAAAiklEQVQYGVXBRwKCMABFwU8QFbtgwV6wV/Dd/26GZKMzspIbUC5r8swB79mWs4VVHEbDN8+arC6MVWm8Wcpac5Q3pDSSLqTyImhJKujLC6Ej6UQmL4ampBkPI2fFXVb9Q25kjWGkSgKPrJ8egamc5IPzgomcaH4urpuuyWGqX8EeBvoV7FjoT9AzXxZnEVySl7A0AAAAAElFTkSuQmCC) white no-repeat center";
      icon.style.border = "1px solid #000";
      icon.style.width = "30px";
      icon.style.height = "30px";
      icon.style.cursor = "pointer";
      icon.title = "Dessiner à main levée";

      var pather = new L.Pather({
        mode: L.Pather.MODE.CREATE | L.Pather.MODE.EDIT | L.Pather.MODE.APPEND,
      });

      icon.addEventListener("click", function() {
        if (active) {
          map.removeLayer(pather);
          active = false;
        } else {
          map.addLayer(pather);
          active = true;
        }
      });

      return container;
    },
  });

  //new FreeDrawControl().addTo(w.map);
}
