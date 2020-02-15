import 'leaflet/dist/leaflet.css';

import L from 'leaflet';

import Config from './config';
import * as Layers from './layers';
import CadastralParcel from './models/cadastralParcel';

const saveJson = (data, fname) => {
  data = encodeURIComponent(JSON.stringify(data));
  data = `data:text/json;charset=utf-8,${data}`;
  let link = document.createElement('a');
  link.setAttribute('href', data);
  link.setAttribute('download', fname);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const createMap = (cfg) => {
  Config.apiKeys = cfg.apiKeys;

  let map = L.map('map').setView([cfg.map.lat, cfg.map.lng], cfg.map.zoom);
  Layers.addSatellite(map);
  Layers.addCadastralParcels(map);
  let bordersLayer = L.geoJSON().addTo(map);

  map.on('click', e => {
    CadastralParcel.fromLatLng(e.latlng)
    .then(parcel => parcel.shape())
    .then(geojson => bordersLayer.addData(geojson));
  });

  document.querySelector('#export-borders').addEventListener(
    'click', e => saveJson(bordersLayer.toGeoJSON(), 'borders.json')
  );
};

const loadProject = id => fetch(`/data/${id}/config.json`)
  .then(resp => resp.json())
  .then(createMap);

loadProject('montfranc');
