<template>
  <div>
    <div class="toolbar">
      <router-link
        :to="{ name: 'project/map/borders', params: { pid: project.id } }"
      >
        Bordures
      </router-link>
    </div>
    <router-view :project="project"/>
    <div class="map">
      <Map
        :apiKey="project.apiKeys.ign"
        :initialZoom="project.map.zoom"
        :initialLat="project.map.lat"
        :initialLng="project.map.lng"
      />
    </div>
  </div>
</template>

<script>
import Map from '@/components/map/Map'

export default {
  components: {
    Map,
  },
  computed: {
    project() {
      return this.$store.state.project
    }
  },
}
</script>

<style scoped>
.map {
  height: 400px;
}
</style>
