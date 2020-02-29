import json

from django.forms import CharField
from django.core.validators import MinValueValidator, MaxValueValidator

from .widgets import MapSetupWidget


class MapSetupField(CharField):
    widget = MapSetupWidget

    def to_python(self, value):
        if not value:
            return None
        return json.loads(value)
