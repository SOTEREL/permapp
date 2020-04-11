<template>
  <div>
    <div v-if="loading">
      Loading...
    </div>
    <div v-else-if="httpErr">
      {{ httpErr }}
    </div>
    <div v-else>
      <div class="toolbar"></div>
      <router-view :project="project" />
      <FeatureList />
      <div class="map">
        <Map />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import FeatureList from "@/components/FeatureList";
import Map from "@/components/map/Map";

export default {
  components: {
    FeatureList,
    Map,
  },

  data() {
    return {
      httpErr: null,
      loading: true,
    };
  },

  computed: mapState({
    project: state => state.project,
  }),

  created() {
    this.fetchMap();
  },

  methods: {
    async fetchMap() {
      this.loading = true;
      this.httpErr = null;
      try {
        await this.$store.dispatch("map/load");
      } catch (e) {
        this.httpErr = {
          code: e.response.status,
          message: e.response.statusText,
        };
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.map {
  height: 400px;
}
</style>
