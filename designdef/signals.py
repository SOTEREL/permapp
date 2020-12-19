from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *  # noqa: F403


@receiver(post_save, sender=ThemedElementType)  # noqa: F405
def create_element_type_style(sender, instance, created, **kwargs):
    if not created:
        return
    style_cls = instance.shape_cls.style_cls
    if style_cls is None:
        raise ValueError(
            f"Unknow style class for shape model {instance.shape_cls.__name__}()"
        )
    style_cls.objects.create(themed_element_type=instance)
