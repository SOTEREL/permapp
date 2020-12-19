from django.apps import AppConfig


class DesignDefConfig(AppConfig):
    name = "designdef"

    def ready(self):
        from . import signals  # noqa
