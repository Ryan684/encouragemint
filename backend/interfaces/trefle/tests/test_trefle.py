import json
from unittest.mock import patch, Mock

import requests
from django.test import TestCase, override_settings

from backend.interfaces.trefle.exceptions import TrefleConnectionError
from backend.interfaces.trefle.trefle import lookup_plants


@override_settings(TREFLE_API_KEY="Foo")
class TestTrefle(TestCase):
    def setUp(self):
        test_responses_dir = "backend/interfaces/trefle/tests/test_responses"
        with open(f"{test_responses_dir}/plant_search_one_match.json", "r") as file:
            self.search_single_match = json.load(file)
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            self.search_many_matches = json.load(file)
        with open(f"{test_responses_dir}/id_search_response.json", "r") as file:
            self.id_search = json.load(file)

        patcher = patch("requests.get")
        self.mock_get = patcher.start()
        self.addCleanup(patcher.stop)

    def test_trefle_unreachable(self):
        self.mock_get.side_effect = requests.exceptions.ConnectionError

        self.assertRaises(
            TrefleConnectionError,
            lookup_plants, {"q": "Fooflower"}
        )

    def test_search_plants_no_results(self):
        self.mock_get.return_value = []

        response = lookup_plants({"q": "Barflower"})

        self.assertEqual([], response)

    def test_lookup_plants_one_result(self):
        self.mock_get.return_value = self.search_single_match
        expected_plant = self.search_single_match

        response = lookup_plants({"scientific_name": "common woolly sunflower"})
        self.assertEqual(expected_plant, response)

    def test_lookup_plants_many_results(self):
        self.mock_get.return_value = self.search_many_matches

        response = lookup_plants({"q": "grass"})

        self.assertEqual(self.search_many_matches, response)

    def test_lookup_plants_by_multiple_properties(self):
        self.mock_get.return_value = self.search_many_matches

        response = lookup_plants({"shade_tolerance": "High", "moisture_use": "High"})

        self.assertEqual(self.search_many_matches, response)
