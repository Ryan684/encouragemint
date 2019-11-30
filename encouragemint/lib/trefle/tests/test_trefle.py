import json
from unittest.mock import patch, Mock

from django.test import TestCase
from requests.exceptions import ConnectionError

from encouragemint.lib.trefle.trefle import TrefleAPI


class TestTrefle(TestCase):
    def setUp(self):
        self.trefle = TrefleAPI()
        with open("encouragemint/lib/trefle/tests/test_responses/name_search_response.json", "r") as name_file:
            self.name_search = json.load(name_file)
        with open("encouragemint/lib/trefle/tests/test_responses/id_search_response.json", "r") as id_search_file:
            self.id_search = json.load(id_search_file)

    @patch("requests.get")
    def test_trefle_unreachable(self, mock_get):
        mock_get.side_effect = ConnectionError
        self.assertRaises(
            ConnectionError,
            self.trefle.lookup_plants_by_scientific_name, "Fooflower"
        )

    @patch("requests.get")
    def test_lookup_plant_common_name(self, mock_get):
        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = self.name_search
        mock_responses[1].json.return_value = self.id_search
        mock_get.side_effect = mock_responses

        plant_name = "common woolly sunflower"
        response = self.trefle.lookup_plants_by_common_name(plant_name)

        self._validate_plant(response)

    @patch("requests.get")
    def test_lookup_plant_by_scientific_name(self, mock_get):
        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = self.name_search
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
            "bloom_period": None,
            "growth_period": None,
            "growth_rate": None,
            "shade_tolerance": None,
            "moisture_use": None,
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
