from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from .feature_type import FeatureType
from .shapes.style import ShapeStyle
from .validators import validate_shape_ctype


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    feature_types = models.ManyToManyField(FeatureType, through="FeatureStyle",)

    def __str__(self):
        return self.name


class FeatureStyle(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    feature_type = models.ForeignKey(FeatureType, on_delete=models.CASCADE)
    shape_ctype = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="+",
        validators=[validate_shape_ctype],
    )
    style = models.OneToOneField(ShapeStyle, on_delete=models.PROTECT)

    # TODO: define zoom range so that we can have different styles depending on
    # the zoom level

    def __str__(self):
        return self.feature_type

    @classmethod
    def validate_style(cls, shape_ctype, style):
        shape_cls = shape_ctype.model_class()
        shape_style_cls = shape_cls.style_cls
        style_cls = style.__class__
        if not issubclass(style_cls, shape_style_cls):
            raise ValidationError(
                f"The style 'style_cls.__name__'  does not apply to the shape '{shape_cls.__name__}'."
            )

    def clean(self):
        self.validate_style(self.shape_ctype, self.style)
