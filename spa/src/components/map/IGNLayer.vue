<template>
  <GeoportalLayer
    layer="GEOGRAPHICALGRIDSYSTEMS.PLANIGN"
    style_="normal"
    format="image/jpeg"
    layer-type="base"
    name="Carte IGN"
  />
</template>

<script>
import GeoportalLayer from "./GeoportalLayer";

export default {
  components: { GeoportalLayer },
};
</script>
