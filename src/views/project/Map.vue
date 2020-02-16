<template>
  <div class="map">
    <Map
      :apiKey="config.apiKeys.ign"
      :initialZoom="config.map.zoom"
      :initialLat="config.map.lat"
      :initialLng="config.map.lng"
    />
  </div>
</template>

<script>
import Map from '@/components/map/Map'

export default {
  components: {
    Map,
  },
  props: [
    'config',
  ],
  data() {
    return {

    }
  }
}
</script>

<style scoped>
.map {
  height: 400px;
}
</style>
