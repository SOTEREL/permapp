from .feature import Feature
from ..fields import LatField, LngField


class Point(Feature):
    lat = LatField()
    lng = LngField()

    @property
    def center(self):
        return dict(lat=self.lat, lng=self.lng)

    @property
    def geojson_geom(self):
        return {"type": "Point", "coordinates": [self.lng, self.lat]}
