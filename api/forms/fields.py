import json

from django.forms import CharField


class AggregationField(CharField):
    def __init__(self, aggregated_fields, *, hide_subfields=True, **kwargs):
        self.aggregated_fields = aggregated_fields
        self.hide_subfields = hide_subfields
        super().__init__(**kwargs)

    def to_python(self, value):
        if not value:
            return None
        return json.loads(value)
