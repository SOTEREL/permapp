from .base import read_env

env = read_env()

CORS_ORIGIN_WHITELIST = ["http://localhost:8080", "http://127.0.0.1:8080"]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"]
}

# https://geoservices.ign.fr/documentation/geoservices/wmts.html
IGN_API_KEY = env.str("IGN_API_KEY")


def get_ign_tile_url(layer):
    return f"https://wxs.ign.fr/{IGN_API_KEY}/geoportail/wmts?service=WMTS&request=GetTile&version=1.0.0&tilematrixset=PM&tilematrix={{z}}&tilecol={{x}}&tilerow={{y}}&layer={layer}&format=image/jpeg&style=normal"


LEAFLET_CONFIG = {
    "DEFAULT_CENTER": (46, 1.5),
    "DEFAULT_ZOOM": 6,
    "MIN_ZOOM": 6,
    "MAX_ZOOM": 18,
    "RESET_VIEW": False,
    "TILES": [
        ("Carte", get_ign_tile_url("GEOGRAPHICALGRIDSYSTEMS.MAPS"), "IGN-F/Géoportail"),
        ("Satellite", get_ign_tile_url("ORTHOIMAGERY.ORTHOPHOTOS"), "IGN-F/Géoportail"),
    ],
    "PLUGINS": {
        "geosearch": {
            "css": ["https://unpkg.com/leaflet-geosearch@3.1.0/dist/geosearch.css"],
            "js": ["https://unpkg.com/leaflet-geosearch@3.1.0/dist/geosearch.umd.js"],
            "auto-include": True,
        },
        "admin_custom": {
            "css": ["designs/admin/leaflet_custom.css"],
            "js": ["designs/admin/leaflet_custom.js"],
            "auto-include": True,
        },
    },
}
