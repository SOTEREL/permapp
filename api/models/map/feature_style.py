from django.core.exceptions import ValidationError
from django.db import models

from jsonfield import JSONField
import jsonschema

from .feature_type import FeatureType


class FeatureStyle(models.Model):
    name = models.CharField(max_length=50)
    feature_type = models.ForeignKey(FeatureType, on_delete=models.CASCADE)
    style = JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = "feature styles"
        unique_together = ("name", "feature_type")

    def __str__(self):
        return f"{self.name} ({self.feature_type})"

    def validate_style(self, value):
        schema = self.feature_type.shape_model.STYLE_SCHEMA
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(str(e))

    def clean(self):
        super().clean()
        self.validate_style(self.style)
