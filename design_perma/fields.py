from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def add_validator_if_not_exist(validators, validator):
    for existing in validators:
        if type(existing) == type(validator):
            return validators
    validators.append(validator)
    return validators


class LngField(models.FloatField):
    def __init__(self, *args, **kwargs):
        # Otherwise, the validator is added multiple times
        validators = kwargs.get("validators", [])
        add_validator_if_not_exist(validators, MinValueValidator(-180))
        add_validator_if_not_exist(validators, MaxValueValidator(180))
        kwargs["validators"] = validators
        super().__init__(*args, **kwargs)


class LatField(models.FloatField):
    def __init__(self, *args, **kwargs):
        validators = kwargs.get("validators", [])
        add_validator_if_not_exist(validators, MinValueValidator(0))
        add_validator_if_not_exist(validators, MaxValueValidator(90))
        kwargs["validators"] = validators
        super().__init__(*args, **kwargs)
