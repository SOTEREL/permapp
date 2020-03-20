from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapDrawingWidget


def make_form(model, extra_js=None):
    js = ("api/js/widgets/feature-map.js",)
    if extra_js is None:
        js = (
            *js,
            "api/js/widgets/{feature}-map.js".format(feature=model.geom_type.lower()),
        )
    else:
        js = (*js, *extra_js)

    FeatureMapWidget = type(
        f"{model.__name__}MapWidget",
        (MapDrawingWidget,),
        {
            "js_args": {"geom_type": model.geom_type},
            "Media": type("Media", (), {"js": js}),
        },
    )

    return type(
        f"{model.__name__}Form",
        (ProjectMapForm,),
        {
            "map": AggregationField(
                ["coordinates", "map_projection", "path_options"],
                widget=FeatureMapWidget,
            ),
            "Meta": type(
                "Meta",
                (),
                {
                    "model": model,
                    "fields": [
                        "project",
                        "name",
                        "category",
                        "map",
                        "description",
                        "permanence",
                    ],
                },
            ),
        },
    )
