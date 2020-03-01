import json

from django.forms import HiddenInput

from .fields import AggregationField
from .widgets import MapWidget


class AggregationFormMixin:
    @classmethod
    def _make_clean_method(cls, aggregation, aggregated):
        def clean(self):
            return self.fields[aggregated].clean(
                self.cleaned_data[aggregation][aggregated]
            )

        return clean

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
                self.fields[aggregated].required = False
                self.fields[aggregated].disabled = True
                setattr(
                    self.__class__,
                    f"clean_{aggregated}",
                    self._make_clean_method(name, aggregated),
                )
            field.initial = json.dumps(initial)


class ProjectMapFormMixin:
    project_field_name = "project"

    def __init__(self):
        project = None
        if self.instance is not None:
            project = getattr(self.instance, self.project_field_name, None)

        try:
            project_field_id = self.fields[self.project_field_name]
        except KeyError:
            project_field_id = None

        print(project, self.is_bound)

        for name, field in self.fields.items():
            if isinstance(field.widget, MapWidget):
                continue
