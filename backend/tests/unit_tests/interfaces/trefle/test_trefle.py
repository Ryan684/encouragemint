import json
from unittest.mock import patch

import requests
from django.test import TestCase, override_settings

from backend.interfaces.trefle.exceptions import TrefleConnectionError
from backend.interfaces.trefle import trefle


@override_settings(TREFLE_API_KEY="Foo")
class TestTrefle(TestCase):
    def setUp(self):
        test_responses_dir = "backend/tests/unit_tests/interfaces/trefle/test_responses"
        with open(f"{test_responses_dir}/plant_search_one_match.json", "r") as file:
            self.search_single_match = json.load(file)
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            self.search_many_matches = json.load(file)
        with open(f"{test_responses_dir}/id_search_response.json", "r") as file:
            self.id_search = json.load(file)

        patcher = patch("requests.get")
        self.mock_get = patcher.start()
        self.addCleanup(patcher.stop)
        self.trefle_payload = {"shade_tolerance": "Tolerant"}

    def test_trefle_unreachable(self):
        # When more error-specific behavior is introduced, this needs to be more specific.
        # I.E, if retry logic is added, we'll need to define separate tests for valid retry errors & non retry errors.
        self.mock_get.side_effect = requests.exceptions.RequestException

        self.assertRaises(TrefleConnectionError, trefle.lookup_plants, self.trefle_payload)

    def test_search_plants_no_results(self):
        self.mock_get.return_value.json.return_value = []

        response = trefle.lookup_plants(self.trefle_payload)

        self._assert_trefle_api_payload(self.trefle_payload)
        self.assertEqual([], response)

    def test_lookup_plants_one_result(self):
        self.mock_get.return_value.json.return_value = self.search_single_match
        expected_plant = self.search_single_match

        response = trefle.lookup_plants(self.trefle_payload)

        self._assert_trefle_api_payload(self.trefle_payload)
        self.assertEqual(expected_plant, response)

    def test_lookup_plants_many_results(self):
        self.mock_get.return_value.json.return_value = self.search_many_matches

        response = trefle.lookup_plants(self.trefle_payload)

        self._assert_trefle_api_payload(self.trefle_payload)
        self.assertEqual(self.search_many_matches, response)

    def test_lookup_plants_by_multiple_properties(self):
        self.mock_get.return_value.json.return_value = self.search_many_matches
        payload = self.trefle_payload.copy()
        payload["moisture_use"] = "High"

        response = trefle.lookup_plants(payload)

        self._assert_trefle_api_payload(payload)
        self.assertEqual(self.search_many_matches, response)

    def _assert_trefle_api_payload(self, search_parameters):
        parameters = {"token": None, "page_size": 100}
        for parameter in search_parameters:
            parameters[f"filter[{parameter}]"] = search_parameters[parameter]

        self.mock_get.assert_called_once_with(
            headers=trefle.HEADERS,
            params=parameters,
            url=trefle.PLANTS_ENDPOINT
        )
