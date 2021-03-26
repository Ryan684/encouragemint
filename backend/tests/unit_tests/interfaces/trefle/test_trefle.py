import json
from unittest.mock import patch

from django.test import TestCase, override_settings

from backend import seasons
from backend.interfaces.trefle import trefle


@override_settings(TREFLE_API_KEY="Foo")
class TestTrefle(TestCase):
    def setUp(self):
        test_responses_dir = "backend/tests/unit_tests/interfaces/trefle/test_responses"
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            self.search_many_matches = json.load(file)
        with open(f"{test_responses_dir}/id_search_response.json", "r") as file:
            self.id_search = json.load(file)

        patcher = patch("requests.get")
        self.mock_get = patcher.start()
        self.addCleanup(patcher.stop)
        self.trefle_payload = {"duration": "Annual"}

    def test_search_plants_no_results(self):
        self.mock_get.return_value.json.return_value = []

        response = trefle.lookup_plants(self.trefle_payload)

        self._assert_trefle_api_call(self.trefle_payload)
        self.assertEqual([], response)

    def test_lookup_plants_many_results(self):
        self.mock_get.return_value.json.return_value = self.search_many_matches

        response = trefle.lookup_plants(self.trefle_payload)

        self._assert_trefle_api_call(self.trefle_payload)
        self.assertEqual(self.search_many_matches, response)

    def test_lookup_plants_by_multiple_properties(self):
        self.mock_get.return_value.json.return_value = self.search_many_matches
        payload = self.trefle_payload.copy()
        payload["bloom_months"] = seasons.BLOOM_MONTHS[seasons.EARLY_SPRING]

        response = trefle.lookup_plants(payload)

        self._assert_trefle_api_call(payload)
        self.assertEqual(self.search_many_matches, response)

    def _assert_trefle_api_call(self, search_parameters):
        parameters = {"token": None, "page_size": 100}
        for parameter in search_parameters:
            parameters[f"filter[{parameter}]"] = search_parameters[parameter]

        self.mock_get.assert_called_once_with(
            headers=trefle.HEADERS,
            params=parameters,
            url=trefle.PLANTS_ENDPOINT
        )
