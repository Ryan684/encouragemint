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
            self.trefle.lookup_plants, {"q": "Fooflower"}
        )

    @patch("requests.get")
    def test_search_plants_no_results(self, mock_get):
        mock_get.return_value = []

        response = self.trefle.lookup_plants({"q": "Barflower"})

        self.assertEqual([], response)

    @patch("requests.get")
    def test_lookup_plants_one_result(self, mock_get):
        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = self.search_single_match
        mock_responses[1].json.return_value = self.id_search
        mock_get.side_effect = mock_responses
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

        response = self.trefle.lookup_plants({"scientific_name": "common woolly sunflower"})

        self.assertEqual(test_plant, response)

    @patch("requests.get")
    def test_lookup_plants_many_results(self, mock_get):
        mock_get.return_value = self.search_many_matches

        response = self.trefle.lookup_plants({"q": "grass"})

        self.assertEqual(self.search_many_matches, response)

    @patch("requests.get")
    def test_lookup_plants_by_multiple_properties(self, mock_get):
        mock_get.return_value = self.search_many_matches

        response = self.trefle.lookup_plants({"shade_tolerance": "High", "moisture_use": "High"})

        self.assertEqual(self.search_many_matches, response)
