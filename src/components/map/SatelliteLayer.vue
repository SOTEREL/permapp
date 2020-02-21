<template>
  <GeoportalLayer
    layer="ORTHOIMAGERY.ORTHOPHOTOS"
    styl="normal"
    format="image/jpeg"
  />
</template>

<script>
import GeoportalLayer from "./GeoportalLayer";

export default {
  modelKey: "satellite",
  components: { GeoportalLayer },
};
</script>
