from django.apps import AppConfig


class DesignsConfig(AppConfig):
    name = "designs"

    def ready(self):
        from . import signals  # noqa
