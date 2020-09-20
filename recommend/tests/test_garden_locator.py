from unittest.mock import patch, Mock

from django.test import TestCase

from recommend.exceptions import GeocoderNoResultsError
from recommend.garden_locator import get_coordinates


class TestGetCoordinates(TestCase):
    def setUp(self):
        patcher = patch("geopy.geocoders.googlev3.GoogleV3.geocode")
        self.mock_geocoder = patcher.start()
        self.addCleanup(patcher.stop)
        self.dummy_location = "Truro, Cornwall"

    def test_no_results(self):
        self.mock_geocoder.return_value = None

        self.assertRaises(GeocoderNoResultsError, get_coordinates, self.dummy_location)

    def test_location_found(self):
        sample_garden_geocode_location = {
            "address": "Truro, Cornwall",
            "latitude": 50.263195,
            "longitude": -5.051041
        }
        
        mock = Mock(**sample_garden_geocode_location)
        self.mock_geocoder.return_value = mock

        latitude, longitude, address = get_coordinates(self.dummy_location)

        self.assertEqual(sample_garden_geocode_location["latitude"], latitude)
        self.assertEqual(sample_garden_geocode_location["longitude"], longitude)
        self.assertEqual(sample_garden_geocode_location["address"], address)
