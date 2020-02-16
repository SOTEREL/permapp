<template>
  <div>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-if="!httpError.code">
        <div class="menu">
          <router-link :to="{ name: 'project', params: { pid: $route.params.pid }}">
            Project
          </router-link>
          <router-link :to="{ name: 'projectMap', params: { pid: $route.params.pid }}">
            Carte
          </router-link>
        </div>

        <router-view :config="config"/>
      </div>
      <Error v-else-if="httpError.code == 404">
        Cannot find project {{ $route.params.pid }}
      </Error>
      <Error v-else>
        Error: {{ httpError.message }} 
      </Error>
    </div>
  </div>
</template>

<script>
import ProjectApi from '@/api/project'
import Error from '@/components/Error'

export default {
  components: {
    Error,
  },
  data() {
    return {
      httpError: {
        code: null,
        message: '',
      },
      loading: true,
      config: null,
    }
  },
  created() {
    this.fetchProject()
  },
  methods: {
    fetchProject() {
      this.loading = true
      this.httpError.code = null
      return ProjectApi.load(this.$route.params.pid)
        .then(config => {
          this.config = config
        })
        .catch(err => {
          this.httpError.message = err.response.statusText
          this.httpError.code = err.response.status
        })
        .finally(_ => {
          this.loading = false
        })
    }
  }
}
</script>
