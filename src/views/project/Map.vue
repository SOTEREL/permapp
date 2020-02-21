<template>
  <div>
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <div class="toolbar">
        <router-link
          :to="{ name: 'project/map/borders', params: { pid: project.id } }"
        >
          Bordures
        </router-link>
      </div>
      <router-view :project="project" />
      <div class="map">
        <Map
          :api-key="project.apiKeys.ign"
          :initial-zoom="map.setup.zoom"
          :initial-lat="map.setup.lat"
          :initial-lng="map.setup.lng"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import Map from "@/components/map/Map";

export default {
  components: {
    Map
  },
  data() {
    return {
      httpErr: null,
      loading: true
    };
  },
  computed: mapState({
    map: state => state.map,
    project: state => state.project
  }),
  created() {
    this.fetchMap();
  },
  methods: {
    fetchMap() {
      this.loading = true;
      this.httpErr = null;
      this.$store
        .dispatch("map/load", this.project.id)
        .catch(err => {
          this.httpErr = {
            code: err.response.status,
            message: err.response.statusText
          };
        })
        .finally(() => {
          this.loading = false;
        });
    }
  }
};
</script>

<style scoped>
.map {
  height: 400px;
}
</style>
