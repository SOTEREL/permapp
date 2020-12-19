from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MapElementType, Theme


@receiver(post_save, sender=MapElementType)
def create_element_type_style(sender, instance, created, **kwargs):
    if not created:
        return
    style_cls = instance.shape_cls.style_cls
    if style_cls is None:
        raise ValueError(
            f"Unknow style class for shape model {instance.shape_cls.__name__}()"
        )
    for theme in Theme.objects.all():
        style_cls.objects.create(map_element_type=instance, theme=theme)
