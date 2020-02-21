<template>
  <l-tile-layer
    v-if="apiKey"
    :url="url"
    attribution="<a href=&quot;https://www.geoportail.gouv.fr/&quot;>geoportail.gouv.fr</a>"
    :options="options"
  />
</template>

<script>
import { LTileLayer } from "vue2-leaflet";

export default {
  components: { LTileLayer },
  props: {
    apiKey: {
      type: String,
      required: true,
    },
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
  data() {
    return {
      options: {
        maxZoom: 19
      },
      url:
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
    };
  }
};
</script>
