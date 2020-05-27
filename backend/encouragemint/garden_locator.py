import logging

from django.conf import settings
from geopy import GoogleV3
from geopy.exc import GeopyError

from backend.encouragemint.exceptions import GeocoderNoResultsError, GardenSystemError, \
    GardenUserError
from backend.encouragemint.models.garden import Garden
from backend.encouragemint.notifications import email
from backend.encouragemint.notifications.email import send_garden_location_not_found_email

logger = logging.getLogger("django")


def register_garden_coordinates(garden_id):
    garden = Garden.objects.get(garden_id=garden_id)
    logger.info(f"Attempting to retrieve coordinates for garden {garden.garden_id}...")

    try:
        latitude, longitude, location = _lookup_garden_coordinates(garden.location)
    except GeopyError as exception:
        raise GardenSystemError(
            f"Adding coordinates failed for garden {garden.garden_id}: {exception}")
    except GeocoderNoResultsError:
        _rollback_garden_creation(garden)
        raise GardenUserError(
            f"Adding coordinates failed for garden {garden.garden_id}. "
            "Could not find a location for that address.")

    _register_garden(garden, latitude, location, longitude)


def _lookup_garden_coordinates(location):
    geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY)
    geo_location = geolocator.geocode(location)

    if geo_location:
        return geo_location.latitude, geo_location.longitude, geo_location.address
    raise GeocoderNoResultsError()


def _rollback_garden_creation(garden):
    garden.delete()
    send_garden_location_not_found_email(
        garden.profile.email_address,
        garden.garden_name,
        garden.profile.first_name,
        garden.location
    )


def _register_garden(garden, latitude, location, longitude):
    garden.latitude = latitude
    garden.longitude = longitude
    garden.location = location
    garden.save()

    logger.info(f"Added coordinates to garden {garden.garden_id} successfully.")
    email.send_garden_registered_email(
        garden.profile.email_address, garden.garden_name, garden.profile.first_name)
