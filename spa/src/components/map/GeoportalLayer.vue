<template>
  <l-tile-layer
    :url="url"
    attribution='<a href="https://www.geoportail.gouv.fr/">geoportail.gouv.fr</a>'
    :options="options"
    :layer-type="layerType"
    :name="name"
  />
</template>

<script>
import { mapState } from "vuex";
import { LTileLayer } from "vue2-leaflet";

import { API_KEYS } from "@/constants";

export default {
  components: { LTileLayer },

  props: {
    layer: {
      type: String,
      required: true,
    },
    style_: {
      type: String,
      required: true,
    },
    format: {
      type: String,
      required: true,
    },
    name: {
      type: String,
    },
    layerType: {
      type: String,
      default: "base",
    },
  },

  data() {
    return {
      options: {
        maxZoom: 19,
      },
    };
  },

  computed: {
    url() {
      return (
        `https://wxs.ign.fr/${API_KEYS.geoportal}/geoportail/wmts?` +
        `REQUEST=GetTile&` +
        `SERVICE=WMTS&` +
        `VERSION=1.0.0&` +
        `TILEMATRIXSET=PM&` +
        `LAYER=${this.layer}&` +
        `STYLE=${this.style_}&` +
        `FORMAT=${this.format}&` +
        `TILECOL={x}&` +
        `TILEROW={y}&` +
        `TILEMATRIX={z}`
      );
    },
  },
};
</script>
