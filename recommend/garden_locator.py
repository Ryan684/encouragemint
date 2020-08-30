from django.conf import settings
from geopy import GoogleV3

from recommend.exceptions import GeocoderNoResultsError


def get_coordinates(location):
    geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY)
    geo_location = geolocator.geocode(location)

    if geo_location:
        return geo_location.latitude, geo_location.longitude, geo_location.address
    raise GeocoderNoResultsError()
