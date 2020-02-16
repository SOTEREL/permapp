import L from 'leaflet';

import Store from './store';

const MAX_ZOOM = 19;

export const addSatellite = map => L.tileLayer(
  'https://wxs.ign.fr/{apiKey}/geoportail/wmts?REQUEST=GetTile' +
  '&SERVICE=WMTS&VERSION=1.0.0&TILEMATRIXSET=PM&LAYER={layer}' +
  '&STYLE={style}&FORMAT={format}' +
  '&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}',
  {
    apiKey: Store.project.config.apiKeys.ign,
    layer: 'ORTHOIMAGERY.ORTHOPHOTOS',
    style: 'normal',
    format: 'image/jpeg',
    maxZoom: MAX_ZOOM,
  }
).addTo(map);

export const addCadastralParcels = map => L.tileLayer(
  'https://wxs.ign.fr/{apiKey}/geoportail/wmts?REQUEST=GetTile' +
  '&SERVICE=WMTS&VERSION=1.0.0&TILEMATRIXSET=PM&LAYER={layer}' +
  '&STYLE={style}&FORMAT={format}' +
  '&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}',
  {
    apiKey: Store.project.config.apiKeys.ign,
    layer: 'CADASTRALPARCELS.PARCELS',
    style: 'bdparcellaire',
    format: 'image/png',
    maxZoom: MAX_ZOOM,
  }
).addTo(map);
