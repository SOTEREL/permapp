var Config = {
  apiKey: 'choisirgeoportail',
  mapSetup: {
    center: {
      x: 2.663316,
      y: 44.190317,
      projection: 'CRS:84'
    },
    zoom: 19
  }
};

(function() {
  var map = Gp.Map.load(
    'map',
    {           
      apiKey: Config.apiKey,
      center: Config.mapSetup.center,
      zoom: Config.mapSetup.zoom,
      layersOptions: {
        'ORTHOIMAGERY.ORTHOPHOTOS' : {},
        'CADASTRALPARCELS.PARCELS': {}
      },
      controlsOptions: {
        'search': {
          maximised: true
        }
      },
    }    
) ;
})();
