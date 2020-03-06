from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapDrawingWidget


def make_form(model):
    class FeatureMapWidget(MapDrawingWidget):
        class Media:
            js = (
                "api/js/widgets/{feature}-map.js".format(
                    feature=model.geom_type.lower()
                ),
            )

    class FeatureForm(ProjectMapForm):
        map = AggregationField(["coordinates"], widget=FeatureMapWidget)

        class Meta:
            model = model
            fields = ["project", "name", "map", "description", "style"]

    return FeatureForm
