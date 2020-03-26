from django.contrib import admin

from ...models.map import DrawingClass


@admin.register(DrawingClass)
class DrawingClassAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
