function getStyle() {
  var styleDiv = document.querySelector(".field-json_str_style");
  if (styleDiv === null) {
    return;
  }
  styleDiv.style.display = "none";
  return JSON.parse(styleDiv.querySelector(".readonly").innerText);
}

window.addEventListener("map:init", function(e) {
  var map = e.detail.map;
  var field = document.getElementById("id_shape-0-edit_zoom");
  var style = getStyle();

  // We need to wait a bit because django-leaflet sets the zoom to 15 for an
  // unknown reason.
  setTimeout(function() {
    map.setZoom(parseInt(field.value));

    map.on("zoomend", function() {
      field.value = map.getZoom();
    });
  }, 500);

  map.on("map:loadfield", function(e) {
    var field = e.field;
    field.drawnItems.eachLayer(function(layer) {
      layer.setStyle(style);
    });
  });
});
