from django.forms import CharField

from ...fields import AggregationField
from ...widgets import MapDrawingWidget
from .shape import ShapeForm, ShapeMapForm


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
                ["coordinates", "map_projection", "zoom"], widget=FeatureMapWidget
            ),
            "Meta": type("Meta", (), {"model": model, "fields": ["map"]}),
        },
    )


class GeoJSONShapeMapForm(ShapeMapForm):
    coordinates = CharField()
    shape_fields = [*ShapeMapForm.shape_fields, "coordinates"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def shape_form_class(self):
        return make_geojson_form(self.shape_class)
