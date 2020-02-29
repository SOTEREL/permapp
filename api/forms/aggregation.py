import json

from django.forms import CharField, HiddenInput


class AggregationField(CharField):
    field = None

    def __init__(self, aggregated_fields, *args, **kwargs):
        self.aggregated_fields = aggregated_fields
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return None
        return json.loads(value)


def _make_clean_method(aggregation, aggregated):
    def clean(self):
        return self.fields[aggregated].clean(self.cleaned_data[aggregation][aggregated])

    return clean


class AggregationFormMixin:
    def __init__(self):
        for name, field in self.fields.items():
            if not isinstance(field, AggregationField):
                continue

            initial = {}
            for aggregated in field.aggregated_fields:
                initial[aggregated] = self.get_initial_for_field(
                    self.fields[aggregated], aggregated
                )
                self.fields[aggregated].widget = HiddenInput()
                setattr(
                    self.__class__,
                    f"clean_{aggregated}",
                    _make_clean_method(name, aggregated),
                )
            field.initial = json.dumps(initial)
