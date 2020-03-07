from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapDrawingWidget


def make_form(model):
    FeatureMapWidget = type(
        f"{model.__name__}MapWidget",
        (MapDrawingWidget,),
        {
            "js_args": {"geom_type": model.geom_type},
            "Media": type(
                "Media",
                (),
                {
                    "js": (
                        "api/js/widgets/feature-map.js",
                        "api/js/widgets/{feature}-map.js".format(
                            feature=model.geom_type.lower()
                        ),
                    )
                },
            ),
        },
    )

    return type(
        f"{model.__name__}Form",
        (ProjectMapForm,),
        {
            "map": AggregationField(
                ["coordinates", "projection"], widget=FeatureMapWidget
            ),
            "Meta": type(
                "Meta",
                (),
                {
                    "model": model,
                    "fields": ["project", "name", "map", "description", "style"],
                },
            ),
        },
    )
