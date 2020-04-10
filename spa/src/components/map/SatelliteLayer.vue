<template>
  <GeoportalLayer
    layer="ORTHOIMAGERY.ORTHOPHOTOS"
    style_="normal"
    format="image/jpeg"
    layer-type="base"
    name="Satellite"
  />
</template>

<script>
import GeoportalLayer from "./GeoportalLayer";

export default {
  components: { GeoportalLayer },
};
</script>
