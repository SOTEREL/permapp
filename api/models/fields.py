from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class LngField(models.FloatField):
    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [
            *kwargs.get("validators", []),
            MinValueValidator(-180),
            MaxValueValidator(180),
        ]
        super().__init__(*args, **kwargs)


class LatField(models.FloatField):
    def __init__(self, *args, **kwargs):
        kwargs["validators"] = [
            *kwargs.get("validators", []),
            MinValueValidator(0),
            MaxValueValidator(90),
        ]
        super().__init__(*args, **kwargs)
