from .feature import Feature
from ..fields import LatField, LngField


class PointBase(Feature):
    lat = LatField()
    lng = LngField()

    class Meta:
        abstract = True

    @property
    def center(self):
        return dict(lat=self.lat, lng=self.lng)

    @property
    def geojson_geom(self):
        return {"type": "Point", "coordinates": [self.lng, self.lat]}


class Point(PointBase):
    pass
