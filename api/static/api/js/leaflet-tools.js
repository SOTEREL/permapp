var LeafletTools = (function() {
  var GEOPORTAL_API_KEY = "choisirgeoportail";

  return {
    geoportal: {
      SatelliteLayer: function(name, style, format) {
        return L.tileLayer(
          "https://wxs.ign.fr/{apiKey}/geoportail/wmts?" +
            "REQUEST=GetTile&" +
            "SERVICE=WMTS&" +
            "VERSION=1.0.0&" +
            "TILEMATRIXSET=PM&" +
            "LAYER={name}&" +
            "STYLE={style}&" +
            "FORMAT={format}&" +
            "TILECOL={x}&" +
            "TILEROW={y}&" +
            "TILEMATRIX={z}",
          {
            apiKey: GEOPORTAL_API_KEY,
            maxZoom: 19,
            attribution:
              '<a href="https://www.geoportail.gouv.fr/">geoportail.gouv.fr</a>',
            name: name,
            style: style,
            format: format,
          }
        );
      },
    },
  };
})();
