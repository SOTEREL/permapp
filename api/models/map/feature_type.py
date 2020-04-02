from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from .category import Category
from .feature_style import FeatureStyle
from .validators import validate_feature_ctype, validate_shape_ctype


class FeatureType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    shape_ctype = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="+",
        validators=[validate_shape_ctype],
    )
    feature_ctype = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="+",
        validators=[validate_feature_ctype],
    )
    style = models.ForeignKey(
        FeatureStyle, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name_plural = "feature types"

    @classmethod
    def list_shape_ctypes(cls):
        from .shapes import Shape  # Import here to avoid circular import

        for ctype in ContentType.objects.all():
            model = ctype.model_class()
            if model is not None and issubclass(model, Shape):
                yield ctype

    @classmethod
    def list_feature_ctypes(cls):
        from .feature import Feature  # Import here to avoid circular import

        for ctype in ContentType.objects.all():
            model = ctype.model_class()
            if model is not None and issubclass(model, Feature):
                yield ctype

    def __str__(self):
        return self.name

    @property
    def shape_model(self):
        return self.shape_ctype.model_class()

    @property
    def feature_model(self):
        return self.feature_ctype.model_class()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if self.pk is not None:
            saved_instance = self.__class__.objects.get(pk=self.pk)
            for field in ("shape_ctype", "feature_ctype"):
                if getattr(saved_instance, field) != getattr(self, field):
                    raise ValidationError(f"Cannot modify {field} field")

    def validate_style(self, value):
        if value is None:
            return
        if value.shape_ctype != self.shape_ctype:
            raise ValidationError(
                f"The style {value} applies to another shape type than {self.shape_ctype}"
            )

    def clean(self):
        super().clean()
        self.validate_style(self.style)
