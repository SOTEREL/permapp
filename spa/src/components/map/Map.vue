<template>
  <LMap
    :zoom="zoom"
    :center="center"
    @update:zoom="z => (zoom = z)"
    @update:center="c => (center = c)"
    @update:bounds="b => (bounds = b)"
  >
    <l-control-layers position="topleft" />
    <IGNLayer />
    <SatelliteLayer />
    <CadastralLayer />
    <BordersLayer />
    <l-geo-json
      v-for="fid in shownFeatureIds"
      :key="fid"
      :geojson="featureDrawings[fid].shape.geojson_geom"
      :options-style="featureDrawings[fid].style.style"
    />
  </LMap>
</template>

<script>
import "leaflet/dist/leaflet.css";

import { mapState } from "vuex";
import { LMap, LControlLayers, LGeoJson } from "vue2-leaflet";

import BordersLayer from "./BordersLayer";
import CadastralLayer from "./CadastralLayer";
import IGNLayer from "./IGNLayer";
import SatelliteLayer from "./SatelliteLayer";

export default {
  components: {
    LMap,
    LControlLayers,
    LGeoJson,
    BordersLayer,
    CadastralLayer,
    IGNLayer,
    SatelliteLayer,
  },

  data() {
    return {
      zoom: null,
      center: null,
      bounds: null,
    };
  },

  computed: {
    ...mapState({
      featureDrawings: state => state.map.featureDrawings,
      shownFeatureIds: state => state.map.view.features,
      initialZoom: state => state.map.view.zoom,
      initialCenter: state => [state.map.view.lat, state.map.view.lng],
    }),
  },

  created() {
    this.zoom = this.initialZoom;
    this.center = this.initialCenter;
  },
};
</script>
