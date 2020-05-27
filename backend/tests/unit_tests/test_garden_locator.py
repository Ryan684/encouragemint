from unittest.mock import patch, Mock

from django.core import mail
from django.test import TestCase
from geopy.exc import GeocoderServiceError

from backend.src.exceptions import GardenUserError, GardenSystemError
from backend.src.garden_locator import register_garden_coordinates
from backend.src.models.garden import Garden
from backend.tests.helpers import SAMPLE_GARDEN_GEOCODE_LOCATION, create_test_garden


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

        self.assertTrue(Garden.objects.filter(garden_id=self.garden_id))
        self.assertEqual(1, len(mail.outbox))  # assert garden registered email was sent.

    def test_unsuccessful_register_garden_coordinates_from_geocoder_exception(self):
        self.mock_google.side_effect = GeocoderServiceError

        self.assertRaises(GardenSystemError, register_garden_coordinates, self.garden_id)
        self.assertEqual(0, len(mail.outbox))  # assert no email was sent - this is a retry scenario.

    def test_unsuccessful_register_garden_coordinates_from_geocoder_location_not_found(self):
        self.mock_google.return_value = None

        self.assertTrue(Garden.objects.filter(garden_id=self.garden_id))
        self.assertRaises(GardenUserError, register_garden_coordinates, self.garden_id)
        self.assertFalse(Garden.objects.filter(garden_id=self.garden_id))
        self.assertEqual(1, len(mail.outbox))  # assert garden not found email was sent.
