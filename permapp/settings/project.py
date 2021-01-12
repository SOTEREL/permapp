from django.utils.translation import gettext_lazy as _

from .base import read_env


env = read_env()

LEAFLET_DEFAULT_PROJECTION = "EPSG:3857"
FEATURE_PERMANENCE_MAX = 10
DEFAULT_SHAPE_EDIT_ZOOM = 18
DEFAULT_PROJECT_ZOOM = 17

PERMANENCE_CHOICES = (
    (None, _("Unspecified")),
    (0, _("Extremely simple to change")),
    (1, _("Simple to change")),
    (2, _("Moderately painful to change")),
    (3, _("Painful to change")),
    (5, _("Unchangeable")),
)
