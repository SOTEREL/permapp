from django.contrib import admin

from ...models.map import CustomType, Type


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "slug",
        "category",
    )
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CustomType)
class CustomTypeAdmin(TypeAdmin):
    fields = (
        "project",
        "name",
        "slug",
        "category",
    )
