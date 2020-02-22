<template>
  <LMap
    :zoom="zoom"
    :center="center"
    @update:zoom="zoomUpdated"
    @update:center="centerUpdated"
    @update:bounds="boundsUpdated"
  >
    <component
      :is="id + '-background'"
      v-for="id in view.backgrounds"
      :key="'background/' + id"
      v-bind="features.background[id]"
    />
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

import { mapState, mapGetters } from "vuex";

import { LMap } from "vue2-leaflet";

import SatelliteLayer from "./SatelliteLayer";
import CadastralLayer from "./CadastralLayer";

const mapBackgrounds = layers =>
  layers.reduce(
    (acc, layer) => ({ ...acc, [layer.modelKey + "-background"]: layer }),
    {}
  );

export default {
  components: {
    LMap,
    ...mapBackgrounds([SatelliteLayer, CadastralLayer]),
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
  computed: mapState({
    features: state => state.map.features,
    interaction: state => state.map.interaction,
    view: state => state.map.view,
  }),
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
