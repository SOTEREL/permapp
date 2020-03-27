from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from jsonfield import JSONField
import jsonschema

from shapely.geometry import shape

from .feature_type import FeatureType
from ..category import Category
from ..drawing_class import DrawingClass
from ...project import Project


class Feature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    comments = models.TextField(default="", blank=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    type = models.ForeignKey(
        FeatureType, null=True, blank=True, on_delete=models.SET_NULL
    )
    drawing_class = models.ForeignKey(
        DrawingClass, null=True, blank=True, on_delete=models.SET_NULL
    )

    coordinates = JSONField()
    map_projection = models.CharField(
        max_length=50, default=settings.LEAFLET_DEFAULT_PROJECTION
    )
    path_options = JSONField(default=dict, blank=True)

    is_risky = models.BooleanField(default=False)
    permanence = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(settings.FEATURE_PERMANENCE_MAX)],
    )
    extra_props = JSONField(default=dict, blank=True)

    @classmethod
    def default_category(cls):
        # Import from here to avoid circular import
        from ..default_category import DefaultCategory

        try:
            return DefaultCategory.objects.get(feature_model=cls.__name__).category
        except DefaultCategory.DoesNotExist:
            return None

    @classmethod
    def default_drawing_class(cls):
        # Import from here to avoid circular import
        from ..default_drawing_class import DefaultDrawingClass

        try:
            return DefaultDrawingClass.objects.get(
                feature_model=cls.__name__
            ).drawing_class
        except DefaultDrawingClass.DoesNotExist:
            return None

    def __init_subclass__(cls, *, geom_type=None, is_generic=False, **kwargs):
        # geom_type is only defined for abstract shape classes
        if geom_type is not None:
            cls.geom_type = geom_type
        cls.is_generic = is_generic

    def __str__(self):
        return self.name

    def validate_coordinates(self, value):
        raise NotImplementedError(
            f"{self.__class__.__name__}.validate_coordinates() must be implemented"
        )

    def validate_extra_props(self, value):
        if self.type is None:
            return
        schema = self.type.extra_props_schema
        try:
            jsonschema.validate(value, schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValidationError(str(e))

    def clean(self):
        super().clean()
        self.validate_coordinates(self.coordinates)
        self.validate_extra_props(self.extra_props)

    @property
    def centroid(self):
        return shape(self.geojson_geom).centroid

    @property
    def perimeter(self):
        return shape(self.geojson_geom).length

    @property
    def area(self):
        return shape(self.geojson_geom).area

    @property
    def geojson_geom(self):
        return {"type": self.geometry_type, "coordinates": self.coordinates}

    @property
    def geojson_props(self):
        return {
            "type": slugify(self.__class__.__name__),
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "options": self.path_options,
            "projection": self.projection,
        }

    @property
    def geojson(self):
        return {
            "type": "Feature",
            "geometry": self.geojson_geom,
            "properties": self.geojson_props,
        }


def attachment_path(instance, filename):
    return f"feature_{instance.feature.id}/{filename}"


class FeatureAttachment(models.Model):
    feature = models.ForeignKey(
        Feature, on_delete=models.CASCADE, related_name="attachments"
    )
    upload = models.FileField(upload_to=attachment_path)
    comments = models.TextField(default="", blank=True)
