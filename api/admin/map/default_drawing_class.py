from django.contrib import admin

from ...models.map import DefaultDrawingClass


@admin.register(DefaultDrawingClass)
class DefaultDrawingClassAdmin(admin.ModelAdmin):
    pass
