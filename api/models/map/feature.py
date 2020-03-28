from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from jsonfield import JSONField
import jsonschema

from .feature_type import FeatureType
from ..project import Project


class Feature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    # What it describes
    type = models.ForeignKey(
        FeatureType, null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=50)
    comments = models.TextField(default="", blank=True)
    is_risky = models.BooleanField(default=False)
    permanence = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(settings.FEATURE_PERMANENCE_MAX)],
    )
    extra_props = JSONField(default=dict, blank=True)

    # How it is drawn
    # drawing_class = models.ForeignKey(
    #    DrawingClass, null=True, blank=True, on_delete=models.SET_NULL
    # )
    # drawing_options = JSONField(default=dict, blank=True)

    def __str__(self):
        return self.name

    @property
    def shape_model(self):
        return self.shape.__class__

    def validate_extra_props(self, value):
        if self.type is None or value is None:
            return

        schema = self.type.extra_props_schema
        if schema is None:
            return

        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(str(e))

    def clean(self):
        super().clean()
        self.validate_extra_props(self.extra_props)


def attachment_path(instance, filename):
    return f"feature_{instance.feature.id}/{filename}"


class FeatureAttachment(models.Model):
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name="attachments"
    )
    upload = models.FileField(upload_to=attachment_path)
    comments = models.TextField(default="", blank=True)


@receiver(post_save, sender=Feature)
def create_shape(sender, instance, created, **kwargs):
    if created and instance.type and instance.type.shape_model:
        instance.shape_model.objects.create(feature=instance)
