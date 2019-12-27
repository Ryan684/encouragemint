import json
from unittest.mock import patch, Mock
from requests.exceptions import ConnectionError

from django.test import TestCase, override_settings

from encouragemint.lib.trefle.exceptions import TrefleConnectionError
from encouragemint.lib.trefle.trefle import TrefleAPI


def get_mock_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


@override_settings(TREFLE_API_KEY="Foo")
class TestTrefle(TestCase):
    def setUp(self):
        self.trefle = TrefleAPI()
        self.search_single_match = get_mock_json_file(
            "encouragemint/lib/trefle/tests/test_responses/plant_search_one_match.json")
        self.search_many_matches = get_mock_json_file(
            "encouragemint/lib/trefle/tests/test_responses/plant_search_many_matches.json")
        self.id_search = get_mock_json_file(
            "encouragemint/lib/trefle/tests/test_responses/id_search_response.json")

    @patch("requests.get")
    def test_trefle_unreachable(self, mock_get):
        mock_get.side_effect = ConnectionError
        self.assertRaises(
            TrefleConnectionError,
            self.trefle.lookup_plants_by_scientific_name, "Fooflower"
        )

    @patch("requests.get")
    def test_search_plants_one_result(self, mock_get):
        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = self.search_single_match
        mock_responses[1].json.return_value = self.id_search
        mock_get.side_effect = mock_responses

        plant_name = "common woolly sunflower"
        response = self.trefle.lookup_plants_by_expected_name(plant_name)

        self._validate_plant(response)

    @patch("requests.get")
    def test_search_plants_many_results(self, mock_get):
        mock_get.return_value = self.search_many_matches

        search_term = "grass"
        response = self.trefle.lookup_plants_by_expected_name(search_term)

        self.assertEquals(self.search_many_matches, response)

    @patch("requests.get")
    def test_lookup_plant_by_scientific_name(self, mock_get):
        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = self.search_single_match
        mock_responses[1].json.return_value = self.id_search
        mock_get.side_effect = mock_responses

        plant_name = "Eriophyllum lanatum"
        response = self.trefle.lookup_plants_by_scientific_name(plant_name)

        self._validate_plant(response)

    def _validate_plant(self, response):
        test_plant = {
            "trefle_id": 134845,
            "common_name": "common woolly sunflower",
            "duration": "Annual, Perennial",
            "bloom_period": "Spring",
            "growth_period": "Summer",
            "growth_rate": "Slow",
            "shade_tolerance": "High",
            "moisture_use": "High",
            "family_common_name": "Aster family",
            "scientific_name": "Eriophyllum lanatum"
        }

        self.assertEqual(test_plant.get("trefle_id"), response.get("trefle_id"))
        self.assertEqual(test_plant.get("scientific_name"), response.get("scientific_name"))
        self.assertEqual(test_plant.get("common_name"), response.get("common_name"))
        self.assertEqual(test_plant.get("duration"), response.get("duration"))
        self.assertEqual(test_plant.get("bloom_period"), response.get("bloom_period"))
        self.assertEqual(test_plant.get("growth_period"), response.get("growth_period"))
        self.assertEqual(test_plant.get("growth_rate"), response.get("growth_rate"))
        self.assertEqual(test_plant.get("shade_tolerance"), response.get("shade_tolerance"))
        self.assertEqual(test_plant.get("moisture_use"), response.get("moisture_use"))
        self.assertEqual(test_plant.get("family_common_name"), response.get("family_common_name"))
