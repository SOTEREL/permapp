<template>
  <GeoportalLayer
    :api-key="apiKey"
    layer="CADASTRALPARCELS.PARCELS"
    styl="bdparcellaire"
    format="image/png"
  />
</template>

<script>
import GeoportalLayer from "./GeoportalLayer";

export default {
  components: { GeoportalLayer },
  props: {
    apiKey: {
      type: String,
      required: true
    },
  },
};
</script>
