<template>
  <LMap
    :zoom="zoom"
    :center="center"
    @update:zoom="zoomUpdated"
    @update:center="centerUpdated"
    @update:bounds="boundsUpdated"
  >
    <l-control-layers position="topleft"></l-control-layers>
    <IGNLayer />
    <SatelliteLayer />
    <CadastralLayer />
    <component
      :is="feature.type"
      v-for="feature in view.features"
      :key="feature.type + '/' + feature.id"
      v-bind="features[feature.type][feature.id]"
    />
  </LMap>
</template>

<script>
import "leaflet/dist/leaflet.css";

import { mapState } from "vuex";

import { LMap, LControlLayers } from "vue2-leaflet";

import CadastralLayer from "./CadastralLayer";
import IGNLayer from "./IGNLayer";
import SatelliteLayer from "./SatelliteLayer";

export default {
  components: {
    LMap,
    LControlLayers,
    CadastralLayer,
    IGNLayer,
    SatelliteLayer,
  },

  props: {
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

  computed: {
    ...mapState({
      features: state => state.map.features,
      view: state => state.map.view,
    }),
  },

  data() {
    return {
      zoom: this.initialZoom,
      center: [this.initialLat, this.initialLng],
      bounds: null,
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
    },
  },
};
</script>
