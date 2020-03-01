import json

from django.forms import CharField


class AggregationField(CharField):
    def __init__(self, aggregated_fields, *args, **kwargs):
        self.aggregated_fields = aggregated_fields
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return None
        return json.loads(value)
