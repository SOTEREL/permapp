<template>
  <div class="home">
    <!--
    <Map
      apiKey="choisirgeoportail"
      :initialZoom="13"
      :initialLat="47"
      :initialLng="2"
    />
    -->
    <ProjectList />
  </div>
</template>

<script>
import ProjectList from '@/components/ProjectList'

export default {
  name: "Home",
  components: {
    ProjectList
  }
};
</script>
