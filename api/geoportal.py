from django.conf import settings
import requests


class ParcelCoordinatesNotFoundError(ValueError):
    pass


def parcel_coordinates(insee, section, number):
    resp = requests.get(
        "https://apicarto.ign.fr/api/cadastre/parcelle",
        params={
            "apikey": settings.GEOPORTAL_API_KEY,
            "code_insee": insee,
            "section": section,
            "numero": number,
        },
    )
    if resp.status_code != 200:
        raise ParcelCoordinatesNotFoundError()
    geojson = resp.json()
    return geojson["features"][0]["geometry"]["coordinates"]
