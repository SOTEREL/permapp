window.addEventListener("map:init", function(e) {
  var map = e.detail.map;
  map.addControl(
    new GeoSearch.GeoSearchControl({
      notFoundMessage: "Adresse inconnue.",
      provider: new GeoSearch.OpenStreetMapProvider(),
      searchLabel: "Entrer une adresse",
      showMarker: false,
      style: "bar",
    })
  );
});
