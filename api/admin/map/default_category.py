from django.contrib import admin

from ...models.map import DefaultCategory


@admin.register(DefaultCategory)
class DefaultCategoryAdmin(admin.ModelAdmin):
    pass
