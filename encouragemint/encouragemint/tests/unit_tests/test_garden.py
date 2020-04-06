from unittest.mock import patch, Mock

from django.test import TestCase
from geopy.exc import GeocoderServiceError
from rest_framework import status

from encouragemint.encouragemint.exceptions import GardenUserError, GardenSystemError
from encouragemint.encouragemint.garden import create_garden
from encouragemint.encouragemint.models.profile import Profile
from encouragemint.encouragemint.tests.helpers import SAMPLE_GARDEN_GEOCODE_LOCATION, SAMPLE_GARDEN, \
    SAMPLE_GARDEN_SUNLIGHT


class TestGarden(TestCase):
    def setUp(self):
        self.location = "Truro, UK"
        profile_object = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})
        self.profile = str(profile_object.profile_id)
        self.garden_data = SAMPLE_GARDEN.copy()
        self.garden_data["profile"] = self.profile

        patcher = patch("geopy.geocoders.googlev3.GoogleV3.geocode")
        self.mock_google = patcher.start()
        self.addCleanup(patcher.stop)

    def test_successful_create_garden(self):
        mock = Mock(**SAMPLE_GARDEN_GEOCODE_LOCATION)
        self.mock_google.return_value = mock

        response = create_garden(self.garden_data)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn("garden_id", response.data)
        self.assertIn("profile", response.data)
        self.assertEqual(SAMPLE_GARDEN.get("garden_name"), response.data.get("garden_name"))
        self.assertEqual(SAMPLE_GARDEN.get("direction"), response.data.get("direction"))
        self.assertEqual(SAMPLE_GARDEN_SUNLIGHT, response.data.get("sunlight"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("address"),
                         response.data.get("location"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("longitude"),
                         response.data.get("longitude"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("latitude"),
                         response.data.get("latitude"))

    def test_unsuccessful_create_garden_from_geocoder_exception(self):
        self.mock_google.side_effect = GeocoderServiceError

        self.assertRaises(GardenSystemError, create_garden, self.garden_data)

    def test_unsuccessful_create_garden_from_geocoder_location_not_found(self):
        self.mock_google.return_value = None

        self.assertRaises(GardenUserError, create_garden, self.garden_data)
