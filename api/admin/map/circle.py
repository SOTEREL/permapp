from django.contrib import admin

from .feature import FeatureAbstractAdmin
from ...models.map import Circle
from ...forms.map import CircleForm


@admin.register(Circle)
class CircleAdmin(FeatureAbstractAdmin):
    form = CircleForm
