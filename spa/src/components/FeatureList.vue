<template>
  <div class="features">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else>
      <div
        v-for="feature in features"
        :key="feature.id"
        @click="e => toggleFeature(feature.id)"
      >
        <span v-if="shownFeatureIds.includes(feature.id)">[X]</span>
        <span v-else>[]</span>
        {{ feature.name }}
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      loading: true,
      error: null,
    };
  },

  computed: {
    ...mapState({
      features: state => state.map.features,
      featureTypes: state => state.map.featureTypes,
      categories: state => state.map.categories,
      shownFeatureIds: state => state.map.view.features,
    }),
  },

  created() {
    this.load();
  },

  methods: {
    async load() {
      this.loading = true;
      this.error = null;
      try {
        await this.$store.dispatch("map/loadFeatures");
      } catch (e) {
        this.error = e;
      } finally {
        this.loading = false;
      }
    },

    async toggleFeature(fid) {
      try {
        await this.$store.dispatch("map/toggleFeature", fid);
      } catch (e) {
        throw e; // TODO
      }
    },
  },
};
</script>

<style scoped></style>
