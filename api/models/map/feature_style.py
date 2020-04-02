from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from jsonfield import JSONField
import jsonschema

from .validators import validate_shape_ctype


class FeatureStyle(models.Model):
    name = models.CharField(max_length=50, unique=True)
    shape_ctype = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="+",
        validators=[validate_shape_ctype],
    )
    style = JSONField(default=dict, blank=True)

    class Meta:
        verbose_name_plural = "feature styles"

    def __str__(self):
        return self.name

    def validate_style(self, value):
        schema = self.shape_ctype.model_class().STYLE_SCHEMA
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(str(e))

    def clean(self):
        super().clean()
        self.validate_style(self.style)
