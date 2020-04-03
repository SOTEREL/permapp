from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from jsonfield import JSONField
import jsonschema
from polymorphic.models import PolymorphicModel

from .feature_type import FeatureType
from ..project import Project


class Feature(PolymorphicModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    type = models.ForeignKey(FeatureType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    comments = models.TextField(default="", blank=True)
    is_risky = models.BooleanField(default=False)
    permanence = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(settings.FEATURE_PERMANENCE_MAX)],
    )

    def __str__(self):
        return self.name

    @property
    def shape_model(self):
        return self.type.shape_model

    @property
    def feature_model(self):
        return self.type.feature_model

    @property
    def category(self):
        return self.type.category


def attachment_path(instance, filename):
    return f"feature_attachments/feature_{instance.feature.id}/{filename}"


class FeatureAttachment(models.Model):
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name="attachments"
    )
    upload = models.FileField(upload_to=attachment_path)
    comments = models.TextField(default="", blank=True)


@receiver(post_save)
def create_shape(sender, instance, created, **kwargs):
    if not issubclass(sender, Feature):
        return
    if created and instance.type:
        instance.shape_model.objects.create(feature=instance)
