<template>
  <GeoportalLayer
    :apiKey="apiKey"
    layer="CADASTRALPARCELS.PARCELS"
    style_="bdparcellaire"
    format="image/png"
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
