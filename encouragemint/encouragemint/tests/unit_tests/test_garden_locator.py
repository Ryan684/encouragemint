from unittest.mock import patch, Mock

from django.core import mail
from django.test import TestCase
from geopy.exc import GeocoderServiceError

from encouragemint.encouragemint.exceptions import GardenUserError, GardenSystemError
from encouragemint.encouragemint.garden_locator import register_garden_coordinates
from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.tests.helpers import SAMPLE_GARDEN_GEOCODE_LOCATION, create_test_garden


class TestGardenLocator(TestCase):
    def setUp(self):
        self.garden_id = create_test_garden()["garden_id"]

        patcher = patch("geopy.geocoders.googlev3.GoogleV3.geocode")
        self.mock_google = patcher.start()
        self.addCleanup(patcher.stop)

    def test_successful_register_garden_coordinates(self):
        mock = Mock(**SAMPLE_GARDEN_GEOCODE_LOCATION)
        self.mock_google.return_value = mock

        register_garden_coordinates(self.garden_id)

        self.assertTrue(Garden.objects.get(garden_id=self.garden_id))
        self.assertEqual(1, len(mail.outbox))

    def test_unsuccessful_register_garden_coordinates_from_geocoder_exception(self):
        self.mock_google.side_effect = GeocoderServiceError

        self.assertRaises(GardenSystemError, register_garden_coordinates, self.garden_id)

    def test_unsuccessful_register_garden_coordinates_from_geocoder_location_not_found(self):
        self.mock_google.return_value = None

        self.assertRaises(GardenUserError, register_garden_coordinates, self.garden_id)
