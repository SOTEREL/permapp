<template>
  <div>
    <div v-if="loading">
      Loading...
    </div>
    <div v-else-if="httpErr">
      <Error v-if="httpErr.code == 404"> Cannot find project {{ pid }} </Error>
      <Error v-else> Error: {{ httpErr.message }} </Error>
    </div>
    <div v-else>
      <div class="menu">
        <router-link to="/">
          Accueil
        </router-link>
        <router-link :to="{ name: 'project', params: { pid } }">
          Projet
        </router-link>
        <router-link :to="{ name: 'project/map', params: { pid } }">
          Carte
        </router-link>
      </div>

      <router-view :project="project" />
    </div>
  </div>
</template>

<script>
import Error from "@/views/Error";

export default {
  components: {
    Error,
  },

  data() {
    return {
      httpErr: null,
      loading: true,
    };
  },

  computed: {
    pid() {
      return this.$route.params.pid;
    },
    project() {
      return this.$store.state.project;
    },
  },

  created() {
    this.fetchProject();
  },

  methods: {
    async fetchProject() {
      this.loading = true;
      this.httpErr = null;
      try {
        await this.$store.dispatch("project/load", this.pid);
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

<style>
.menu > * {
  margin: 0px 5px;
}
</style>
