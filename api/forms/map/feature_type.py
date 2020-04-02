from django.forms import ALL_FIELDS, ModelForm
from django_json_widget.widgets import JSONEditorWidget

from ...models.map import FeatureType


class FeatureTypeForm(ModelForm):
    class Meta:
        model = FeatureType
        fields = ALL_FIELDS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ctype_fields = {
            "shape_ctype": FeatureType.list_shape_ctypes,
            "feature_ctype": FeatureType.list_feature_ctypes,
        }
        for field, list_ctypes in ctype_fields.items():
            if field in self.fields:
                ctype_ids = [ctype.pk for ctype in list_ctypes()]
                self.fields[field].queryset = self.fields[field].queryset.filter(
                    pk__in=ctype_ids
                )
