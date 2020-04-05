function FeatureMapWidget(config, geomType, drawControlOptions) {
  config.geomType = geomType;
  var mapWidget = MapWidget(config);
  var drawingWidget = MapDrawingWidget(config, mapWidget);

  return {
    mapWidget: mapWidget,
    drawingWidget: drawingWidget,
    init: function() {
      mapWidget.init(
        "Satellite",
        {
          Satellite: MapTools.layers.satellite(),
          IGN: MapTools.layers.ign(),
        },
        {
          Cadastre: MapTools.layers.cadastral(),
        }
      );
      drawingWidget.init(drawControlOptions);
    },
  };
}
