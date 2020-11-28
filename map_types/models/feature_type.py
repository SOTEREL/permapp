from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.utils import OperationalError
from tagging.registry import register as tagging_register


class FeatureType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="", blank=True)
    needs = models.TextField(default="", blank=True)
    contributions = models.TextField(default="", blank=True)

    class Meta:
        verbose_name_plural = "feature types"

    @classmethod
    def list_shape_ctypes(cls):
        from .shapes import Shape  # Import here to avoid circular import

        try:
            for ctype in ContentType.objects.all():
                model = ctype.model_class()
                if (
                    model is not None
                    and model is not Shape
                    and issubclass(model, Shape)
                ):
                    yield ctype
        except OperationalError:  # The table hasn't been created yet
            pass

    @classmethod
    def list_feature_ctypes(cls):
        from .feature import Feature  # Import here to avoid circular import

        try:
            for ctype in ContentType.objects.all():
                model = ctype.model_class()
                if model is not None and issubclass(model, Feature):
                    yield ctype
        except OperationalError:  # The table hasn't been created yet
            pass

    def __str__(self):
        return self.name

    @property
    def shape_model(self):
        return self.shape_ctype.model_class()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)

        if self.pk is not None:
            saved_instance = self.__class__.objects.get(pk=self.pk)
            if saved_instance.shape_ctype != self.shape_ctype:
                raise ValidationError("Cannot modify shape_ctype field")

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


tagging_register(FeatureType)
