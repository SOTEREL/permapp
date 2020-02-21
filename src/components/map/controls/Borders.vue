<template>
  <div>todo {{ borders }}</div>
</template>

<script>
import { mapState } from "vuex";

import L from "leaflet";

export default {
  data() {
    return {
      httpErr: null,
      loading: true,
    };
  },
  computed: mapState({
    borders: state => state.map.borders,
  }),
  created() {
    this.fetchBorders();
    this.$store.dispatch("map/addTiles", ["cadastral"]);
  },
  methods: {
    fetchBorders() {
      this.loading = true;
      this.httpErr = null;
      this.$store
        .dispatch("map/loadBorders")
        .catch(err => {
          this.httpErr = {
            code: err.response.status,
            message: err.response.statusText,
          };
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>
