from . import project
from .map import category, circle, parcel, view
from .map.feature import register_feature_admin
from .. import models


register_feature_admin(models.map.Line)
register_feature_admin(models.map.MultiPolygon)
register_feature_admin(models.map.Point)
register_feature_admin(models.map.Polygon)
