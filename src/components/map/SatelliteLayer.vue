<template>
  <GeoportalLayer
    :api-key="apiKey"
    layer="ORTHOIMAGERY.ORTHOPHOTOS"
    styl="normal"
    format="image/jpeg"
  />
</template>

<script>
import GeoportalLayer from "./GeoportalLayer";

export default {
  components: { GeoportalLayer },
  props: {
    apiKey: {
      type: String,
      required: true,
    },
  },
};
</script>
