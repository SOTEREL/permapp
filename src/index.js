import 'leaflet/dist/leaflet.css';

import L from 'leaflet';

import Config from './config';
import * as Layers from './layers';
import * as Geo from './geo';

const createMap = (cfg) => {
  Config.apiKeys = cfg.apiKeys;

  let map = L.map('map').setView([cfg.map.lat, cfg.map.lng], cfg.map.zoom);
  Layers.addSatellite(map);
  Layers.addCadastralParcels(map);

  Geo.getParcelShapeFromPos([cfg.map.lng, cfg.map.lat])
  .then(console.info);
};

const loadProject = id => fetch(`/data/${id}/config.json`)
  .then(resp => resp.json())
  .then(createMap);

loadProject('montfranc');
