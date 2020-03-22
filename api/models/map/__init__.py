from .category import Category
from .parcel import Parcel
from .view import View, ViewFeature

# GeoJSON features
from .circle import Circle
from .feature import Feature, FeatureAttachment
from .line import Line
from .point import Point
from .polygon import MultiPolygon, Polygon

# Specific features
from .artificial_area import ArtificialArea
from .building import Building
from .pathway import Pathway
from .wall import Wall

# Must be imported AFTER all features, so that they can be registered first
from .default_category import DefaultCategory
