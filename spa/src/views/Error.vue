<template>
  <div>
    <router-link to="/">
      Accueil
    </router-link>
    <div class="error">
      <slot />
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.error {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
