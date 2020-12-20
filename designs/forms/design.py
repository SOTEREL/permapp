from django import forms

from ..models import Design


class DesignAdminForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = forms.ALL_FIELDS
        labels = {"map_center": "Position"}
        widgets = {"map_zoom": forms.HiddenInput()}
