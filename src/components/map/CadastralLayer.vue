<template>
  <GeoportalLayer
    layer="CADASTRALPARCELS.PARCELS"
    styl="bdparcellaire"
    format="image/png"
  />
</template>

<script>
import GeoportalLayer from "./GeoportalLayer";

export default {
  modelKey: "cadastral-geoportal",
  components: { GeoportalLayer },
};
</script>
