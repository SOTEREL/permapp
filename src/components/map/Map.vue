<template>
  <l-map
    :zoom="zoom"
    :center="center"
    @update:zoom="zoomUpdated"
    @update:center="centerUpdated"
    @update:bounds="boundsUpdated"
  >
    <SatelliteLayer :api-key="apiKey" />
    <CadastralLayer :api-key="apiKey" />
  </l-map>
</template>

<script>
import "leaflet/dist/leaflet.css";

import { LMap } from "vue2-leaflet";

import SatelliteLayer from "./SatelliteLayer";
import CadastralLayer from "./CadastralLayer";

export default {
  name: "Map",
  components: {
    LMap,
    SatelliteLayer,
    CadastralLayer
  },
  props: {
    apiKey: {
      type: String,
      required: true,
    },
    initialZoom: {
      type: Number,
      required: true,
    },
    initialLat: {
      type: Number,
      required: true,
    },
    initialLng: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      zoom: this.initialZoom,
      center: [this.initialLat, this.initialLng],
      bounds: null
    };
  },
  methods: {
    zoomUpdated(zoom) {
      this.zoom = zoom;
    },
    centerUpdated(center) {
      this.center = center;
    },
    boundsUpdated(bounds) {
      this.bounds = bounds;
    }
  }
};
</script>
