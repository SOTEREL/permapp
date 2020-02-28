from django.contrib import admin

from categories.base import CategoryBaseAdmin

from ...models.map import Category


@admin.register(Category)
class CategoryAdmin(CategoryBaseAdmin):
    pass
