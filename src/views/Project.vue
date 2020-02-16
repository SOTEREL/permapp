<template>
  <div>
    <div v-if="loading">Loading...</div>
    <Error v-if="!loading && httpErrorCode == 404">
      Cannot find {{ $route.params.id }}
    </Error>
    <div v-if="!loading">
      {{ config }}
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
      httpErrorCode: null,
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
      this.httpErrorCode = null
      return ProjectApi.load(this.$route.params.id)
        .then(config => {
          this.config = config
        })
        .catch(err => {
          this.httpErrorCode = err.response.status
        })
        .finally(_ => {
          this.loading = false
        })
    }
  }
}
</script>
