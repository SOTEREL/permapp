from django.contrib import admin

from ..mixins import LinkToProject
from ...models.map import CustomType, Type


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "category",
    )
    list_display = ("name", "category")


@admin.register(CustomType)
class CustomTypeAdmin(admin.ModelAdmin, LinkToProject):
    fields = (
        "project",
        "name",
        "category",
    )
    list_display = ("name", "link_to_project", "category")
