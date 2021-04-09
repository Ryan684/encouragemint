import json

from unittest.mock import patch, Mock

import requests
from django.test import override_settings, TestCase
from rest_framework import status

from backend.exceptions import GeocoderNoResultsError
from backend.tests import helpers


@override_settings(METEOSTAT_API_KEY="Foo")
@override_settings(GOOGLE_API_KEY="Foo")
class TestApiIntegration(TestCase):
    def setUp(self):
        self.url = "/recommend/"
        self.data = helpers.VALID_RECOMMEND_PAYLOAD

        geocoder_patcher = patch("geopy.geocoders.googlev3.GoogleV3.geocode",
                                 return_value=Mock(**helpers.SAMPLE_GARDEN_GEOCODE_LOCATION))
        self.mock_geocoder = geocoder_patcher.start()
        self.addCleanup(geocoder_patcher.stop)

        get_patcher = patch("requests.get")
        self.mock_get = get_patcher.start()
        self.addCleanup(get_patcher.stop)

        interface_tests_dir = "backend/tests/unit_tests/interfaces"
        self.trefle_responses_dir = f"{interface_tests_dir}/trefle/test_responses"
        self.meteostat_responses_dir = f"{interface_tests_dir}/meteostat/test_responses"

    def test_input_validation_error(self):
        response = self.client.post(f"{self.url}", content_type="application/json", data={"season": "summer"})

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_external_service_request_error(self):
        self.mock_get.side_effect = requests.exceptions.RequestException

        response = self.client.post(f"{self.url}", content_type="application/json", data=self.data)

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

    def test_location_not_found_error(self):
        self.mock_geocoder.side_effect = GeocoderNoResultsError

        response = self.client.post(f"{self.url}", content_type="application/json", data=self.data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {"message": "We couldn't find your location. Please try and be more specific."}, response.json())

    def test_recommendations_found(self):
        with open(f"{self.trefle_responses_dir}/plant_search_many_matches.json", "r") as file:
            trefle_response = json.load(file)
        self._prime_get_rest_mocks(trefle_response)

        response = self.client.post(f"{self.url}", content_type="application/json", data=self.data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(trefle_response, response.json())

    def test_no_recommendations_found(self):
        with open(f"{self.trefle_responses_dir}/plant_search_no_matches.json", "r") as file:
            trefle_response = json.load(file)
        self._prime_get_rest_mocks(trefle_response)

        response = self.client.post(f"{self.url}", content_type="application/json", data=self.data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(trefle_response, response.json())

    def _prime_get_rest_mocks(self, trefle_response):
        mock_meteostat_responses = [Mock(), Mock()]

        with open(f"{self.meteostat_responses_dir}/climate_normals_response.json", "r") as file:
            mock_meteostat_responses[0].json.return_value = json.load(file)
        mock_meteostat_responses[1].json.return_value = trefle_response

        self.mock_get.side_effect = mock_meteostat_responses
