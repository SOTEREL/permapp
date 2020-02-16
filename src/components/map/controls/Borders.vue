<template>
  <div>
    todo {{ project.name }}
  </div>
</template>

<script>
export default {
  computed: {
    project() {
      return this.$store.state.project
    }
  },
  data() {
    return {
    }
  },
  created() {
    this.fetchBorders()
  },
  methods: {
    fetchBorders() {
    }
  },
}
</script>
