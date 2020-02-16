import 'leaflet/dist/leaflet.css';

import L from 'leaflet';

import Store from './store';
import * as Layers from './layers';
import * as Utils from './utils';
import CadastralParcel from './models/CadastralParcel';
import Project from './models/Project';

const setup = (project) => {
  Store.project = project;

  let map = L.map('map').setView(
    [project.config.map.lat, project.config.map.lng],
    project.config.map.zoom
  );
  Layers.addSatellite(map);
  Layers.addCadastralParcels(map);
  let bordersLayer = L.geoJSON().addTo(map);

  map.on('click', e => {
    CadastralParcel.fromLatLng(e.latlng)
    .then(parcel => parcel.shape())
    .then(geojson => bordersLayer.addData(geojson));
  });

  document.querySelector('#export-borders').addEventListener(
    'click', e => Utils.saveJson(bordersLayer.toGeoJSON(), 'borders.json')
  );
};

Project.load('montfranc').then(setup);
