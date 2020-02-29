import json

from django.forms import ModelForm, HiddenInput, ValidationError

from .fields import MapSetupField
from ..models import Project


class ProjectForm(ModelForm):
    map = MapSetupField()

    class Meta:
        model = Project
        fields = ["name", "slug", "map", "map_lat", "map_lng", "map_zoom"]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance", None)
        if instance:
            kwargs.update(
                initial={
                    "map": json.dumps(
                        dict(
                            lat=instance.map_lat,
                            lng=instance.map_lng,
                            zoom=instance.map_zoom,
                        )
                    )
                }
            )

        super().__init__(*args, **kwargs)

        self.fields["map_lat"].widget = HiddenInput()
        self.fields["map_lng"].widget = HiddenInput()
        self.fields["map_zoom"].widget = HiddenInput()

    def clean_map_lat(self):
        return self.fields["map_lat"].clean(self.cleaned_data["map"]["lat"])

    def clean_map_lng(self):
        return self.fields["map_lng"].clean(self.cleaned_data["map"]["lng"])

    def clean_map_zoom(self):
        return self.fields["map_zoom"].clean(self.cleaned_data["map"]["zoom"])
