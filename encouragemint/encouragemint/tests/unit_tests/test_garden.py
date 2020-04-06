from unittest.mock import patch, Mock

from django.test import TestCase
from geopy.exc import GeocoderServiceError

from encouragemint.encouragemint.exceptions import GardenUserError, GardenSystemError
from encouragemint.encouragemint.garden import create_garden
from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.models.profile import Profile
from encouragemint.encouragemint.tests.helpers import SAMPLE_GARDEN_GEOCODE_LOCATION, SAMPLE_GARDEN


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

        self.garden_data["garden_name"] = "task_test_garden"

        create_garden(self.garden_data)

        self.assertTrue(Garden.objects.get(garden_name="task_test_garden"))

    def test_unsuccessful_create_garden_from_geocoder_exception(self):
        self.mock_google.side_effect = GeocoderServiceError

        self.assertRaises(GardenSystemError, create_garden, self.garden_data)

    def test_unsuccessful_create_garden_from_geocoder_location_not_found(self):
        self.mock_google.return_value = None

        self.assertRaises(GardenUserError, create_garden, self.garden_data)
