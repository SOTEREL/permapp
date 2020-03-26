from . import project
from .map import (
    category,
    default_category,
    default_drawing_class,
    drawing_class,
    parcel,
    view,
)
from .map.feature import register_feature_admin
from .. import models


register_feature_admin(
    models.map.Circle,
    extra_js=["api/js/widgets/circle-map.js"],
    map_widget_name="CircleMapWidget",
)
register_feature_admin(models.map.Line)
register_feature_admin(models.map.MultiPolygon)
register_feature_admin(models.map.Point)
register_feature_admin(models.map.Polygon)

register_feature_admin(models.map.Building, extra_fields=["roof_surface"])
register_feature_admin(models.map.Wall, extra_fields=["height"])
register_feature_admin(models.map.ArtificialArea, extra_fields=["surface"])
register_feature_admin(models.map.Pathway, extra_fields=["is_road"])
