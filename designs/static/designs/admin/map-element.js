window.addEventListener("map:init", function(e) {
  var map = e.detail.map;
  var field = document.getElementById("id_shape-0-edit_zoom");

  // We need to wait a bit because django-leaflet sets the zoom to 15 for an
  // unknown reason.
  setTimeout(function() {
    map.setZoom(parseInt(field.value));

    map.on("zoomend", function() {
      field.value = map.getZoom();
    });
  }, 500);
});
