from django import forms


class MapShapeAdminForm(forms.ModelForm):
    class Meta:
        model = None  # Specified by modelform_factory()
        fields = forms.ALL_FIELDS
        widgets = {"edit_zoom": forms.HiddenInput()}
