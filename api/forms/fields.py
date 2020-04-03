import json

from django.contrib.contenttypes.models import ContentType
from django.forms import CharField, ModelChoiceField

from ..models.map import FeatureType


class AggregationField(CharField):
    def __init__(self, aggregated_fields, *, hide_subfields=True, **kwargs):
        self.aggregated_fields = aggregated_fields
        self.hide_subfields = hide_subfields
        super().__init__(**kwargs)

    def to_python(self, value):
        if not value:
            return None
        return json.loads(value)


class CtypeField(ModelChoiceField):
    list_ctypes = None

    def __init__(self, *args, **kwargs):
        queryset = None
        if self.list_ctypes is not None:
            ctype_ids = [ctype.pk for ctype in self.list_ctypes()]
            queryset = ContentType.objects.filter(pk__in=ctype_ids)
        super().__init__(*args, queryset=queryset, **kwargs)


class ShapeCtypeField(CtypeField):
    list_ctypes = FeatureType.list_shape_ctypes


class FeatureCtypeField(CtypeField):
    list_ctypes = FeatureType.list_feature_ctypes
