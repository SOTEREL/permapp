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
  var editZoomField = document.getElementById("id_shape-0-edit_zoom");
  var style = getStyle();

  document.querySelector("#shape-0 .field-edit_zoom").style.display = "none";

  // We need to wait a bit because django-leaflet sets the zoom to 15 for an
  // unknown reason.
  setTimeout(function() {
    map.setZoom(parseInt(editZoomField.value));

    map.on("zoomend", function() {
      editZoomField.value = map.getZoom();
    });
  }, 500);

  map.on("map:loadfield", function(e) {
    var field = e.field;
    field._drawControl.setDrawingOptions({
      polyline: field.options.is_linestring && { shapeOptions: style },
      polygon: field.options.is_polygon && { shapeOptions: style },
      circle: false && { shapeOptions: style },
      rectangle: field.options.is_polygon && { shapeOptions: style },
      marker: field.options.is_point && { shapeOptions: style },
    });
    field.drawnItems.eachLayer(function(layer) {
      layer.setStyle(style);
    });
  });
});
