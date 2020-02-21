<template>
  <LMap
    :zoom="zoom"
    :center="center"
    @update:zoom="zoomUpdated"
    @update:center="centerUpdated"
    @update:bounds="boundsUpdated"
  >
    <component
      :is="layer.key + '-layer'"
      v-for="layer in tiles"
      :key="layer.key"
      v-bind="layer.props"
    />
  </LMap>
</template>

<script>
import "leaflet/dist/leaflet.css";

import { mapState, mapGetters } from "vuex";

import { LMap } from "vue2-leaflet";

import SatelliteLayer from "./SatelliteLayer";
import CadastralLayer from "./CadastralLayer";

const mapLayers = layers =>
  layers.reduce(
    (acc, layer) => ({ ...acc, [layer.modelKey + "-layer"]: layer }),
    {}
  );

export default {
  components: {
    LMap,
    ...mapLayers([SatelliteLayer, CadastralLayer]),
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
    ...mapGetters("map", {
      tiles: "tilesAsObjects",
    }),
    ...mapState({
      features: state => state.map.view.features,
      interaction: state => state.map.interaction,
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
