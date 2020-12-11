from django.apps import AppConfig


class SystemTypesConfig(AppConfig):
    name = "system_types"

    def ready(self):
        from . import signals  # noqa
