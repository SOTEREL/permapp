from django.forms import ModelForm

from ...fields import AggregationField
from ...forms import AggregationForm
from ...widgets import MapWidget, MapDrawingWidget


class ShapeForm(AggregationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is not None and self.instance.feature_id is not None:
            style = self.instance.feature.style
            if style is not None:
                style = style.style

            project = self.instance.feature.project
            map_center = dict(lng=project.map_lng, lat=project.map_lat)

            for field in self.fields.values():
                if isinstance(field.widget, MapWidget):
                    field.widget.add_js_arg("mapCenter", map_center)
                    field.widget.add_js_arg("featureStyle", style)


def make_geojson_form(model, extra_js=None, extra_fields=None, map_widget_name=None):
    js = ("api/js/widgets/feature-map.js",)
    if extra_js is None:
        js = (
            *js,
            "api/js/widgets/{feature}-map.js".format(feature=model.GEOM_TYPE.lower()),
        )
    else:
        js = (*js, *extra_js)

    if map_widget_name is None:
        map_widget_name = f"{model.GEOM_TYPE}MapWidget"

    FeatureMapWidget = type(
        map_widget_name,
        (MapDrawingWidget,),
        {
            "js_args": {"geom_type": model.GEOM_TYPE},
            "Media": type("Media", (), {"js": js}),
        },
    )

    return type(
        f"{model.__name__}Form",
        (ShapeForm,),
        {
            "map": AggregationField(
                ["coordinates", "map_projection"], widget=FeatureMapWidget
            ),
            "Meta": type("Meta", (), {"model": model, "fields": ["map"]}),
        },
    )
