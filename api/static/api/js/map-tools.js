var MapTools = (function() {
  var GEOPORTAL_API_KEY = "choisirgeoportail";

  function makeLayer(name, style, format) {
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
  }

  var geo = {
    center: {},
    geocode: function(location) {
      return new Promise((resolve, reject) => {
        Gp.Services.geocode({
          apiKey: GEOPORTAL_API_KEY,
          location: location,
          filterOptions: {
            type: ["StreetAddress"],
          },
          onSuccess: function(resp) {
            resolve(resp.locations);
          },
          onFailure: reject,
        });
      });
    },
    parcelFromPos: function(pos) {
      return new Promise((resolve, reject) => {
        Gp.Services.reverseGeocode({
          apiKey: GEOPORTAL_API_KEY,
          position: { x: pos.lng, y: pos.lat },
          filterOptions: {
            type: ["CadastralParcel"],
          },
          onSuccess: function(resp) {
            var parcel = resp.locations[0];
            if (parcel === undefined) {
              reject("No parcels found.");
            }
            resolve({
              insee: parcel.placeAttributes.insee,
              section: parcel.placeAttributes.section,
              number: parcel.placeAttributes.number,
            });
          },
          onFailure: reject,
        });
      });
    },
    parcelShape: function(parcel) {
      var url = new URL("https://apicarto.ign.fr/api/cadastre/parcelle");
      url.search = new URLSearchParams({
        apikey: GEOPORTAL_API_KEY,
        code_insee: parcel.insee,
        section: parcel.section,
        numero: parcel.number,
      }).toString();

      return fetch(url)
        .then(function(resp) {
          return resp.json();
        })
        .then(function(geojson) {
          return geojson.features[0].geometry;
        });
    },
  };

  geo.center.fromPoints = function(points) {
    var sumLat = 0;
    var sumLng = 0;
    var n = 0;

    for (var p of points) {
      sumLat += p[1];
      sumLng += p[0];
      n++;
    }

    return {
      lat: sumLat / n,
      lng: sumLng / n,
    };
  };

  geo.center.fromPolygon = function(poly) {
    var externalRing = poly[0];
    return geo.center.fromPoints(externalRing);
  };

  geo.center.fromMultiPolygon = function(multipoly) {
    var points = [];
    var polyCenter;
    for (var poly of multipoly) {
      polyCenter = geo.center.fromPolygon(poly);
      points.push([polyCenter.lng, polyCenter.lat]);
    }
    return geo.center.fromPoints(points);
  };

  return {
    geo: geo,
    layers: {
      satellite: makeLayer("ORTHOIMAGERY.ORTHOPHOTOS", "normal", "image/jpeg"),
      cadastral: makeLayer(
        "CADASTRALPARCELS.PARCELS",
        "bdparcellaire",
        "image/png"
      ),
    },
  };
})();
