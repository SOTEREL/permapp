<template>
  <div>todo {{ project.name }}</div>
</template>

<script>
export default {
  data() {
    return {};
  },
  computed: {
    project() {
      return this.$store.state.project;
    }
  },
  created() {
    this.fetchBorders();
  },
  methods: {
    fetchBorders() {}
  }
};
</script>
