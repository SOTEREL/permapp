from django.forms import ModelForm

from ...fields import AggregationField
from ...forms import AggregationForm
from ...widgets import MapWidget, MapDrawingWidget


class ShapeForm(AggregationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """
        if self.instance is not None:
            for field in self.fields.values():
                if isinstance(field.widget, MapWidget):
                    # TODO: map center based on feature's project
                    field.widget.add_js_arg("project_field_id", None)
        """

    def clean(self):
        super().clean()
        print(self.cleaned_data)
        print(self.errors)


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
