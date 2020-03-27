from django.conf import settings
from django.forms import IntegerField

from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget

from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapDrawingWidget


class FeatureForm(ProjectMapForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        drawing_class = self._meta.model.default_drawing_class()
        if drawing_class is not None:
            self.fields["drawing_class"].initial = drawing_class

        feature_type = self.instance.type
        if feature_type is None:
            self.fields["extra_props"].widget = self.fields[
                "extra_props"
            ].hidden_widget()
        else:
            extra_props_schema = feature_type.extra_props_schema
            self.fields["extra_props"].widget = JSONSchemaWidget(extra_props_schema)


def make_form(model, extra_js=None, extra_fields=None, map_widget_name=None):
    js = ("api/js/widgets/feature-map.js",)
    if extra_js is None:
        js = (
            *js,
            "api/js/widgets/{feature}-map.js".format(feature=model.geom_type.lower()),
        )
    else:
        js = (*js, *extra_js)

    if map_widget_name is None:
        map_widget_name = f"{model.geom_type}MapWidget"

    FeatureMapWidget = type(
        map_widget_name,
        (MapDrawingWidget,),
        {
            "js_args": {"geom_type": model.geom_type},
            "Media": type("Media", (), {"js": js}),
        },
    )

    return type(
        f"{model.__name__}Form",
        (FeatureForm,),
        {
            "map": AggregationField(
                ["coordinates", "map_projection", "path_options"],
                widget=FeatureMapWidget,
            ),
            "permanence": IntegerField(
                required=False, min_value=0, max_value=settings.FEATURE_PERMANENCE_MAX
            ),
            "Meta": type(
                "Meta",
                (),
                {
                    "model": model,
                    "fields": [
                        "project",
                        "name",
                        "type",
                        "drawing_class",
                        "map",
                        "comments",
                        "extra_props",
                        *(extra_fields or []),
                    ],
                },
            ),
        },
    )
