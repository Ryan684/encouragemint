from unittest.mock import patch, Mock

import requests
from django.test import override_settings, TestCase
from rest_framework import status

from backend.exceptions import GeocoderNoResultsError
from backend.tests import helpers


@override_settings(METEOSTAT_API_KEY="Foo")
@override_settings(GOOGLE_API_KEY="Foo")
class TestGarden(TestCase):
    def setUp(self):
        self.url = "/recommend/"
        self.data = {"season": "summer", "direction": "South", "location": "Romsey, UK"}

        geocoder_patcher = patch("geopy.geocoders.googlev3.GoogleV3.geocode",
                                 return_value=Mock(**helpers.SAMPLE_GARDEN_GEOCODE_LOCATION))
        self.mock_geocoder = geocoder_patcher.start()
        self.addCleanup(geocoder_patcher.stop)

        meteostat_patcher = patch("requests.post")
        self.mock_meteostat = meteostat_patcher.start()
        self.addCleanup(meteostat_patcher.stop)

        trefle_patcher = patch("requests.get")
        self.mock_trefle = trefle_patcher.start()
        self.addCleanup(trefle_patcher.stop)

    def test_input_validation_error(self):
        response = self.client.post(f"{self.url}", content_type="application/json", data={"season": "summer"})

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_external_service_connection_error(self):
        self.mock_trefle.side_effect = requests.RequestException

        response = self.client.post(f"{self.url}", content_type="application/json", data=self.data)

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

    def test_location_not_found_error(self):
        self.mock_geocoder.side_effect = GeocoderNoResultsError

        response = self.client.post(f"{self.url}", content_type="application/json", data=self.data)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_single_recommendation_found(self):
        mock_trefle_responses = [Mock(), Mock()]
        mock_trefle_responses[0].json.return_value = helpers.TREFLE_NAME_SINGLE_LOOKUP_RESPONSE
        mock_trefle_responses[1].json.return_value = helpers.TREFLE_ID_LOOKUP_RESPONSE

        self.mock_trefle.side_effect = mock_trefle_responses

        mock_meteostat_responses = [Mock(), Mock()]
        mock_meteostat_responses[0].json.return_value = helpers.METEOSTAT_STATION_SEARCH_RESPONSE
        mock_meteostat_responses[1].json.return_value = helpers.METEOSTAT_STATION_WEATHER_RESPONSE

        self.mock_meteostat.side_effect = mock_meteostat_responses

        response = self.client.post(f"{self.url}", content_type="application/json", data=self.data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_many_recommendations_found(self):
        self.mock_trefle.return_value = helpers.TREFLE_NAME_MULTIPLE_LOOKUP_RESPONSES

        mock_meteostat_responses = [Mock(), Mock()]
        mock_meteostat_responses[0].json.return_value = helpers.METEOSTAT_STATION_SEARCH_RESPONSE
        mock_meteostat_responses[1].json.return_value = helpers.METEOSTAT_STATION_WEATHER_RESPONSE

        self.mock_meteostat.side_effect = mock_meteostat_responses

        response = self.client.post(f"{self.url}", content_type="application/json", data=self.data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_no_recommendations_found(self):
        self.mock_trefle.return_value = []

        mock_meteostat_responses = [Mock(), Mock()]
        mock_meteostat_responses[0].json.return_value = helpers.METEOSTAT_STATION_SEARCH_RESPONSE
        mock_meteostat_responses[1].json.return_value = helpers.METEOSTAT_STATION_WEATHER_RESPONSE

        self.mock_meteostat.side_effect = mock_meteostat_responses

        response = self.client.post(f"{self.url}", content_type="application/json", data=self.data)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
