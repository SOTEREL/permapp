<template>
  <div class="projects">
    <div
      v-for="p in projects"
      :key="p.id"
      class="project"
    >
      <router-link :to="{ name: 'project', params: { pid: p.id } }">
        {{ p.name }}
      </router-link>
    </div>
  </div>
</template>

<script>
import ProjectApi from "@/api/Project";

export default {
  data() {
    return {
      projects: []
    };
  },
  created() {
    this.fetchProjects();
  },
  methods: {
    fetchProjects() {
      return ProjectApi.list().then(projects => {
        this.projects = projects;
      });
    }
  }
};
</script>

<style scoped>
.projects {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
