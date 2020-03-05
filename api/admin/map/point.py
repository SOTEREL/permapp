from django.contrib import admin

from .feature import FeatureAbstractAdmin
from ...models.map import Point
from ...forms.map import PointForm


@admin.register(Point)
class PointAdmin(FeatureAbstractAdmin):
    form = PointForm
