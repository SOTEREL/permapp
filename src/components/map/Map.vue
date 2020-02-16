<template>
  <div class="map">
    <l-map
      :zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated"
    >
      <SatelliteLayer :apiKey="apiKey" />
      <CadastralLayer :apiKey="apiKey" />
    </l-map>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css'

import { LMap } from 'vue2-leaflet'

import SatelliteLayer from './SatelliteLayer'
import CadastralLayer from './CadastralLayer'

export default {
  name: 'Map',
  components: {
    LMap,
    SatelliteLayer,
    CadastralLayer,
  },
  props: [
    'apiKey',
    'initialZoom',
    'initialLat',
    'initialLng',
  ],
  data() {
    return {
      zoom: this.initialZoom,
      center: [this.initialLat, this.initialLng],
      bounds: null,
    }
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
}
</script>

<style scoped>
.map {
  height: 400px;
}
</style>
