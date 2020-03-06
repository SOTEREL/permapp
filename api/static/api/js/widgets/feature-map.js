function FeatureMapWidget(config, geomType, drawControlOptions) {
  config.geomType = geomType;
  var mapWidget = MapWidget(config);
  var drawingWidget = MapDrawingWidget(config, mapWidget);

  mapWidget.init([MapTools.layers.satellite]);
  drawingWidget.init(drawControlOptions);
}
