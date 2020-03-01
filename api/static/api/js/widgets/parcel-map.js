function ParcelMapWidget(mapId, field, kwargs) {
  var projectField = document.getElementById(kwargs.project_field_id);
  var map = L.map(mapId);
  var parcel;
  var loading = false;
  var formRow = django.jQuery("#" + mapId).closest(".form-row");
  var errorUl = django.jQuery('<ul class="errorlist"></ul>');
  formRow.prepend(errorUl);

  function setLoading(isLoading) {
    loading = isLoading;
    if (loading) {
      map.getContainer().style.opacity = 0.1;
      map.getContainer().style.cursor = "progress";
    } else {
      map.getContainer().style.opacity = 1;
      map.getContainer().style.cursor = "pointer";
    }
  }

  function displayError(err) {
    errorUl.html("<li>" + err + "</li>");
  }

  function readData() {
    return JSON.parse(field.value);
  }

  function updateData(data) {
    field.value = JSON.stringify(data);
    if (parcel) map.removeLayer(parcel);
    parcel = L.geoJSON(
      {
        type: "Feature",
        geometry: data.geom,
        properties: {
          insee: data.insee,
          section: data.section,
          number: data.number,
        },
      },
      {
        style: {
          fillColor: "white",
          fillOpacity: 0.5,
          color: "#000",
          weight: 1,
        },
        onEachFeature: function(feature, layer) {
          var html = "";
          for (var k in feature.properties) {
            html +=
              "<div><strong>" +
              k +
              ":</strong> " +
              feature.properties[k] +
              "</div>";
          }
          layer.bindPopup(html);
        },
      }
    ).addTo(map);
    setLoading(false);
  }

  function setMapCenterFromProject() {
    if (projectField) {
      var projectId = projectField.value;
      if (projectId === "") {
        return;
      }
      fetch("/api/projects/" + projectId + "/") // TODO
        .then(function(resp) {
          return resp.json();
        })
        .then(function(project) {
          map.setView([project.map_lat, project.map_lng], project.map_zoom);
        })
        .catch(displayError);
    }
  }

  function getPointsCenter(points) {
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
  }

  function initMapCenter() {
    var geom = readData().geom;
    if (geom) {
      var center = getPointsCenter(geom.coordinates[0][0]);
      map.setView([center.lat, center.lng], 18);
    } else if (!setMapCenterFromProject()) {
      map.setView([46.55886030311719, 2.0654296875000004], 5);
    }
  }

  setLoading(false);
  initMapCenter();
  MapTools.layers.satellite.addTo(map);
  MapTools.layers.cadastral.addTo(map);

  updateData(readData());

  map.on("click", function(e) {
    if (loading) return;
    setLoading(true);
    MapTools.geo
      .parcelFromPos(e.latlng)
      .then(function(parcel) {
        MapTools.geo
          .parcelShape(parcel)
          .then(function(geom) {
            parcel.geom = geom;
            updateData(parcel);
          })
          .catch(function(err) {
            displayError(err);
            setLoading(false);
          });
      })
      .catch(function(err) {
        displayError(err);
        setLoading(false);
      });
  });

  if (projectField) {
    projectField.addEventListener("change", setMapCenterFromProject);
  }
}
