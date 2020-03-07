function FeatureMapWidget(config, geomType, drawControlOptions) {
  config.geomType = geomType;
  var mapWidget = MapWidget(config);
  var drawingWidget = MapDrawingWidget(config, mapWidget);

  return {
    mapWidget: mapWidget,
    drawingWidget: drawingWidget,
    init: function() {
      mapWidget.init([MapTools.layers.satellite]);
      drawingWidget.init(drawControlOptions);
    },
  };
}
