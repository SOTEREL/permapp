from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MapElement, MapElementType, MapTheme


@receiver(post_save, sender=MapElementType)
def create_element_type_style(sender, instance, created, **kwargs):
    if not created:
        return
    style_cls = instance.shape_cls.style_cls
    if style_cls is None:
        raise ValueError(
            f"Unknow style class for shape model {instance.shape_cls.__name__}()"
        )
    for map_theme in MapTheme.objects.all():
        style_cls.objects.create(map_element_type=instance, map_theme=map_theme)


@receiver(post_save, sender=MapElement)
def create_map_element_shape(sender, instance, created, **kwargs):
    if not created:
        return
    shape_cls = instance.element_type.shape_cls
    shape_cls.objects.create(map_element=instance)
