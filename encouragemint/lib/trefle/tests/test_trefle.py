from unittest.mock import patch

from requests.exceptions import ConnectionError
from django.test import TestCase

from encouragemint.lib.trefle.trefle import TrefleAPI


class TestTrefle(TestCase):
    def setUp(self):
        self.trefle = TrefleAPI()

    @patch("requests.get")
    def test_trefle_unreachable(self, mock_get):
        mock_get.side_effect = ConnectionError
        self.assertRaises(
            ConnectionError,
            self.trefle.lookup_plants_by_scientific_name, "Fooflower"
        )

    def test_lookup_plant_common_name(self):
        plant_name = "common woolly sunflower"
        response = self.trefle.lookup_plants_by_common_name(plant_name)

        self._validate_plant(response)

    def test_lookup_plant_by_scientific_name(self):
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
