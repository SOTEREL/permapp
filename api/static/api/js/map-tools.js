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
        maxZoom: 22,
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

  geo.center.fromPoint = function(point) {
    return {
      lng: point[0],
      lat: point[1],
    };
  };

  geo.center.fromLineString = function(points) {
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
    return geo.center.fromLineString(externalRing);
  };

  geo.center.fromMultiPolygon = function(multipoly) {
    var points = [];
    var polyCenter;
    for (var poly of multipoly) {
      polyCenter = geo.center.fromPolygon(poly);
      points.push([polyCenter.lng, polyCenter.lat]);
    }
    return geo.center.fromLineString(points);
  };

  return {
    geo: geo,
    layers: {
      satellite: function() {
        // Need to make a copy in case of multiple maps on the same page
        return makeLayer("ORTHOIMAGERY.ORTHOPHOTOS", "normal", "image/jpeg");
      },
      cadastral: function() {
        return makeLayer(
          "CADASTRALPARCELS.PARCELS",
          "bdparcellaire",
          "image/png"
        );
      },
      ign: function() {
        return makeLayer(
          "GEOGRAPHICALGRIDSYSTEMS.PLANIGN",
          "normal",
          "image/jpeg"
        );
      },
    },
    controls: {
      CompassControl: L.Control.extend({
        options: {
          position: "topright",
        },
        onAdd: function(map) {
          var container = L.DomUtil.create("div", "leaflet-control");
          container.style.backgroundColor = "#FFF";
          container.style.backgroundImage =
            "url('/static/api/compass-rose.png')";
          container.style.width = "40px";
          container.style.height = "40px";
          container.style.border = "1px solid rgba(0,0,0,1)";
          container.style.borderRadius = "2px";
          return container;
        },
      }),
      GeocoderControl: L.Control.extend({
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

          var this_ = this;

          icon.addEventListener("click", function() {
            if (searchContainer.style.display == "none") {
              searchContainer.style.display = "block";
              input.focus();
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
                    this_.options.onSelectLocation(loc);
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
      }),
    },
  };
})();
