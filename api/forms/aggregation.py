import json

from django.forms import ALL_FIELDS, HiddenInput, ModelForm, modelform_factory
from django.forms.models import ModelFormMetaclass

from .fields import AggregationField


class AggregationFormMetaclass(ModelFormMetaclass):
    def __new__(mcs, name, bases, attrs):
        form_cls = super().__new__(mcs, name, bases, attrs)

        form_cls.aggregator_fields = set()
        form_cls.aggregated_fields = set()
        for field_name, field in form_cls.base_fields.items():
            if isinstance(field, AggregationField):
                form_cls.aggregator_fields.add(field_name)
                form_cls.aggregated_fields.update(field.aggregated_fields)

        # Add potential missing aggregated fields
        if form_cls._meta.model:
            model_form = modelform_factory(form_cls._meta.model, fields=ALL_FIELDS)
            for field_name, field in model_form.base_fields.items():
                if (
                    field_name in form_cls.aggregated_fields
                    and field_name not in form_cls.base_fields
                ):
                    form_cls.base_fields[field_name] = field

        return form_cls


class AggregationForm(ModelForm, metaclass=AggregationFormMetaclass):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Attach aggregated fields ids to their parent
        for field_name in self.aggregator_fields:
            field = self.fields[field_name]
            field.widget.subfields = {}
            field.required = False
            for subfield_name in field.aggregated_fields:
                field.widget.subfields[subfield_name] = self[subfield_name].auto_id
                if field.hide_subfields:
                    self.fields[subfield_name].widget = HiddenInput()
