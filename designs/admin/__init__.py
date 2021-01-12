# flake8: noqa
from django.contrib import admin

from tagging.forms import TagAdminForm
from tagging.models import Tag, TaggedItem

from .configuration import *
from .design import *
from .element import *
from .element_type import *
from .map_theme import *
from .map_view import *


# Add autocompletion
# See https://github.com/Fantomas42/django-tagging/pull/21
admin.site.unregister(Tag)
admin.site.unregister(TaggedItem)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    search_fields = ("name",)


@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ("tag",)
