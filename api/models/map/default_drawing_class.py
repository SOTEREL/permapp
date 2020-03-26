from django.apps import apps
from django.db import models

from .drawing_class import DrawingClass
from .features.feature import Feature

features = [
    (model.__name__, model.__name__)
    for model in apps.get_app_config("api").get_models()
    if model is not Feature and issubclass(model, Feature) and not model.is_generic
]


class DefaultDrawingClass(models.Model):
    drawing_class = models.ForeignKey(DrawingClass, on_delete=models.CASCADE)
    feature_model = models.CharField(max_length=50, choices=features, unique=True)

    class Meta:
        verbose_name_plural = "default drawing classes"

    def __str__(self):
        return f"{self.feature_model}: {self.drawing_class}"
