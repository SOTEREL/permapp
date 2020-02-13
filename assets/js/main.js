function init(config) {
  var map = Gp.Map.load(
    'map',
    {           
      apiKey: config.apiKeys.ign,
      center: config.map.center,
      zoom: config.map.zoom,
      layersOptions: {
        'ORTHOIMAGERY.ORTHOPHOTOS' : {},
        'CADASTRALPARCELS.PARCELS': {}
      },
      controlsOptions: {
        'search': {
          maximised: true
        },
        'reversesearch': {
          maximised: true
        }
      },
      mapEventsOptions: {
      },
    }    
  );
}

fetch('/data/montfranc/config.json')
.then(function(resp) {
  return resp.json();
})
.then(init);
