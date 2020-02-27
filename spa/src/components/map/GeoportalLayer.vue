<template>
  <l-tile-layer
    :url="url"
    attribution='<a href="https://www.geoportail.gouv.fr/">geoportail.gouv.fr</a>'
    :options="options"
  />
</template>

<script>
import { mapState } from "vuex";

import { LTileLayer } from "vue2-leaflet";

export default {
  components: { LTileLayer },
  props: {
    layer: {
      type: String,
      required: true,
    },
    styl: {
      type: String,
      required: true,
    },
    format: {
      type: String,
      required: true,
    },
  },
  computed: mapState({
    apiKey: state => state.project.apiKeys.geoportal,
    url(state) {
      return (
        `https://wxs.ign.fr/${this.apiKey}/geoportail/wmts?` +
        `REQUEST=GetTile&` +
        `SERVICE=WMTS&` +
        `VERSION=1.0.0&` +
        `TILEMATRIXSET=PM&` +
        `LAYER=${this.layer}&` +
        `STYLE=${this.styl}&` +
        `FORMAT=${this.format}&` +
        `TILECOL={x}&` +
        `TILEROW={y}&` +
        `TILEMATRIX={z}`
      );
    },
  }),
  data() {
    return {
      options: {
        maxZoom: 19,
      },
    };
  },
};
</script>
