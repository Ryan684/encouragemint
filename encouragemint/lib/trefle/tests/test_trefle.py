from django.test import TestCase

from encouragemint.lib.trefle.trefle import TrefleAPI


class TestTrefle(TestCase):
    def setUp(self):
        self.trefle = TrefleAPI()

    def test_lookup_plant_one_match(self):
        plant_name = "common woolly sunflower"
        expected_plant = {
            "trefle_id": 134845,
            "scientific_name": "Eriophyllum lanatum",
            "duration": "Annual, Perennial",
            "bloom_period": None,
            "growth_period": None,
            "growth_rate": None,
            "shade_tolerance": None,
            "moisture_use": None,
            "family_common_name": "Aster family"
        }

        response = self.trefle.lookup_plant(plant_name)

        self.assertEqual(expected_plant.get("trefle_id"), response.get("trefle_id"))
        self.assertEqual(expected_plant.get("scientific_name"), response.get("scientific_name"))
        self.assertEqual(expected_plant.get("duration"), response.get("duration"))
        self.assertEqual(expected_plant.get("bloom_period"), response.get("bloom_period"))
        self.assertEqual(expected_plant.get("growth_period"), response.get("growth_period"))
        self.assertEqual(expected_plant.get("growth_rate"), response.get("growth_rate"))
        self.assertEqual(expected_plant.get("shade_tolerance"), response.get("shade_tolerance"))
        self.assertEqual(expected_plant.get("moisture_use"), response.get("moisture_use"))
        self.assertEqual(expected_plant.get("family_name"), response.get("family_name"))
