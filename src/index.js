import 'ol/ol.css';

import PointerInteraction from 'ol/interaction/Pointer';
import { toLonLat } from 'ol/proj';
import GeoJSON from 'ol/format/GeoJSON';
import Circle from 'ol/geom/Circle';
import {Vector as VectorLayer} from 'ol/layer';
import {Vector as VectorSource} from 'ol/source';
import {Circle as CircleStyle, Fill, Stroke, Style} from 'ol/style';

import * as Gp from '@ignf-geoportal/sdk-2d';

import {getParcelShapeFromPos, setIGNApiKey} from './GeoUtils';

let map;
const image = new CircleStyle({
  radius: 5,
  fill: null,
  stroke: new Stroke({color: 'red', width: 1})
});
const styles = {
  'Point': new Style({
    image: image
  }),
  'LineString': new Style({
    stroke: new Stroke({
      color: 'green',
      width: 1
    })
  }),
  'MultiLineString': new Style({
    stroke: new Stroke({
      color: 'green',
      width: 1
    })
  }),
  'MultiPoint': new Style({
    image: image
  }),
  'MultiPolygon': new Style({
    stroke: new Stroke({
      color: 'yellow',
      width: 1
    }),
    fill: new Fill({
      color: 'rgba(255, 255, 0, 0.1)'
    })
  }),
  'Polygon': new Style({
    stroke: new Stroke({
      color: 'blue',
      lineDash: [4],
      width: 3
    }),
    fill: new Fill({
      color: 'rgba(0, 0, 255, 0.1)'
    })
  }),
  'GeometryCollection': new Style({
    stroke: new Stroke({
      color: 'magenta',
      width: 2
    }),
    fill: new Fill({
      color: 'magenta'
    }),
    image: new CircleStyle({
      radius: 10,
      fill: null,
      stroke: new Stroke({
        color: 'magenta'
      })
    })
  }),
  'Circle': new Style({
    stroke: new Stroke({
      color: 'red',
      width: 2
    }),
    fill: new Fill({
      color: 'rgba(255,0,0,0.2)'
    })
  })
};

const mapLoaded = evt => {
  map.getLibMap().addInteraction(new PointerInteraction({
    handleDownEvent: e => {
      getParcelShapeFromPos(toLonLat(e.coordinate))
      .then(geojson => map.getLibMap().addLayer(new VectorLayer({
        source: new VectorSource({
          features: (new GeoJSON()).readFeatures(geojson)
        }),
        style: feature => styles[feature.getGeometry().getType()]
      })))
      .catch(console.error);
    }
  }));
};

const createMap = (cfg) => {
  setIGNApiKey(cfg.apiKeys.ign);
  map = Gp.Map.load(
    'map',
    {
      apiKey: cfg.apiKeys.ign,
      enableRotation: true,
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
      mapEventsOptions: { mapLoaded },
    }
  );
};

const loadProject = id => fetch(`/data/${id}/config.json`)
  .then(resp => resp.json())
  .then(createMap);

loadProject('montfranc');
