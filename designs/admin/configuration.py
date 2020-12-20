from django.contrib import admin
from solo.admin import SingletonModelAdmin

from ..models import Configuration


@admin.register(Configuration)
class ConfigurationAdmin(SingletonModelAdmin):
    autocomplete_fields = ("default_theme",)
