<template>
  <l-geo-json
    v-if="borders"
    :geojson="borders.geojson_geom"
    :options-style="style_"
    layer-type="overlay"
    name="Bordures"
  />
</template>

<script>
import { mapState } from "vuex";
import { LGeoJson } from "vue2-leaflet";

export default {
  components: { LGeoJson },

  data() {
    return {
      style_: {
        fill: false,
        stroke: true,
        color: "blue",
        weight: 2,
      },
    };
  },

  computed: {
    ...mapState({
      borders: state => state.map.borders,
    }),
  },

  created() {
    this.load();
  },

  methods: {
    async load() {
      await this.$store.dispatch("map/loadBorders");
    },
  },
};
</script>
