import django.apps
from django.db import models

from .category import Category
from .feature import Feature

features = [
    (model.__name__, model.__name__)
    for model in django.apps.apps.get_models()
    if model is not Feature and issubclass(model, Feature) and not model.is_generic
]


class DefaultCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    feature = models.CharField(max_length=50, choices=features)
