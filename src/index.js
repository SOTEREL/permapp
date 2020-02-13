import * as Geo from '@ignf-geoportal/sdk-2d';

const init = (cfg) => {
  const map = Geo.Map.load('map', {
    apiKey: cfg.apiKeys.ign,
    layersOptions: {
      'ORTHOIMAGERY.ORTHOPHOTOS': {},
      'CADASTRALPARCELS.PARCELS': {},
    },
    center: {
      x: cfg.map.lng,
      y: cfg.map.lat,
      projection: cfg.map.projection,
    },
    zoom: cfg.map.zoom,
  });
};

fetch('/data/montfranc/config.json')
.then(resp => resp.json())
.then(init);
