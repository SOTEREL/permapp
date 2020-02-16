<template>
  <div class="project">
    project home: {{ project.name }}
  </div>
</template>

<script>
export default {
  computed: {
    project() {
      return this.$store.state.project
    }
  },
}
</script>
