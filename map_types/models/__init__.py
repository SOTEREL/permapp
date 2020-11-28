# flake8: noqa

# Monkey-patch django-polymorphic
# See https://github.com/django-polymorphic/django-polymorphic/issues/473
import django
from django.db import models
from polymorphic.base import PolymorphicModelBase


def polymorphic__new__(self, model_name, bases, attrs, **kwargs):
    # Workaround compatibility issue with six.with_metaclass() and custom Django model metaclasses:
    if not attrs and model_name == "NewBase":
        return super(PolymorphicModelBase, self).__new__(
            self, model_name, bases, attrs, **kwargs
        )

    # Make sure that manager_inheritance_from_future is set, since django-polymorphic 1.x already
    # simulated that behavior on the polymorphic manager to all subclasses behave like polymorphics
    if django.VERSION < (2, 0):
        if "Meta" in attrs:
            if not hasattr(attrs["Meta"], "manager_inheritance_from_future"):
                attrs["Meta"].manager_inheritance_from_future = True
        else:
            attrs["Meta"] = type(
                "Meta", (object,), {"manager_inheritance_from_future": True}
            )

    # create new model
    new_class = self.call_superclass_new_method(model_name, bases, attrs, **kwargs)

    # check if the model fields are all allowed
    self.validate_model_fields(new_class)

    # validate resulting default manager
    if not new_class._meta.abstract and not new_class._meta.swapped:
        self.validate_model_manager(new_class.objects, model_name, "objects")

    # for __init__ function of this class (monkeypatching inheritance accessors)
    new_class.polymorphic_super_sub_accessors_replaced = False

    # determine the name of the primary key field and store it into the class variable
    # polymorphic_primary_key_name (it is needed by query.py)
    for f in new_class._meta.fields:
        if f.primary_key and type(f) != models.OneToOneField:
            new_class.polymorphic_primary_key_name = f.name
            break

    return new_class


def polymorphic_call_superclass_new_method(self, model_name, bases, attrs, **kwargs):
    """call __new__ method of super class and return the newly created class.
    Also work around a limitation in Django's ModelBase."""
    # There seems to be a general limitation in Django's app_label handling
    # regarding abstract models (in ModelBase). See issue 1 on github - TODO: propose patch for Django
    # We run into this problem if polymorphic.py is located in a top-level directory
    # which is directly in the python path. To work around this we temporarily set
    # app_label here for PolymorphicModel.
    meta = attrs.get("Meta", None)
    do_app_label_workaround = (
        meta
        and attrs["__module__"] == "polymorphic"
        and model_name == "PolymorphicModel"
        and getattr(meta, "app_label", None) is None
    )

    if do_app_label_workaround:
        meta.app_label = "poly_dummy_app_label"
    new_class = super(PolymorphicModelBase, self).__new__(
        self, model_name, bases, attrs, **kwargs
    )
    if do_app_label_workaround:
        del meta.app_label
    return new_class


PolymorphicModelBase.__new__ = polymorphic__new__
PolymorphicModelBase.call_superclass_new_method = classmethod(
    polymorphic_call_superclass_new_method
)


from .feature_style import FeatureStyle
from .feature_type import FeatureType
from .shapes.geojson_shape import *
from .shapes.shape import Shape
