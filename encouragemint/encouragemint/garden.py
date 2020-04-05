import logging

from django.conf import settings
from django.forms import model_to_dict
from geopy import GoogleV3
from geopy.exc import GeopyError
from rest_framework import status
from rest_framework.response import Response

from encouragemint.encouragemint.exceptions import GeocoderConnectionError, GeocoderNoResultsError
from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.models.profile import Profile

logger = logging.getLogger("django")


def create_garden(garden_data):
    profile = Profile.objects.get(profile_id=garden_data["profile"])
    location = garden_data["location"]

    try:
        garden_data["latitude"], garden_data["longitude"], garden_data["location"] \
            = _lookup_garden_coordinates(location)
    except GeocoderConnectionError as exception:
        logger.error(f"Adding garden failed for profile {profile.profile_id}: {exception}")
        return Response(
            {"Message": "Encouragemint can't create new gardens right now. Try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except GeocoderNoResultsError:
        logger.error(
            f"Adding garden failed for profile {profile.profile_id}. "
            "Could not find a location for that address.")
        return Response(
            {"Message": "Encouragemint couldn't find that location. Try to be more accurate."},
            status=status.HTTP_400_BAD_REQUEST
        )

    garden_data["profile"] = profile
    garden = Garden.objects.create(**garden_data)
    garden_data = model_to_dict(garden)
    garden_data["shade_tolerance"] = garden.shade_tolerance
    garden_data["sunlight"] = garden.sunlight
    logger.info(
        f"Added garden {garden.garden_id} to profile {profile.profile_id} successfully.")
    return Response(garden_data, status=status.HTTP_201_CREATED)


def _lookup_garden_coordinates(location):
    try:
        geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY)
        geo_location = geolocator.geocode(location)

        if geo_location:
            return geo_location.latitude, geo_location.longitude, geo_location.address
        raise GeocoderNoResultsError()
    except GeopyError as exception:
        raise GeocoderConnectionError(exception)