<template>
  <div class="projects">
    <div class="error">
      {{ error }}
    </div>
    <div v-for="p in projects" :key="p.id" class="project">
      <router-link :to="{ name: 'project', params: { pid: p.id } }">
        {{ p.name }}
      </router-link>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  data() {
    return {
      error: null,
    };
  },

  computed: {
    ...mapState({
      projects: state => state.project.list,
    }),
  },

  created() {
    this.load();
  },

  methods: {
    async load() {
      this.error = null;
      try {
        this.$store.dispatch("project/list");
      } catch (e) {
        this.error = e;
      }
    },
  },
};
</script>

<style scoped>
.projects {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
