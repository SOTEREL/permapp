<template>
  <GeoportalLayer
    :apiKey="apiKey"
    layer="ORTHOIMAGERY.ORTHOPHOTOS"
    style_="normal"
    format="image/jpeg"
  />
</template>

<script>
import GeoportalLayer from './GeoportalLayer'

export default {
  components: { GeoportalLayer },
  props: [
    'apiKey'
  ]
}
</script>
