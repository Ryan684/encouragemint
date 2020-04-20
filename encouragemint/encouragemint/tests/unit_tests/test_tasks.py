import json
from unittest.mock import patch, ANY

from celery.exceptions import Retry
from django.test import TestCase

from encouragemint.encouragemint.exceptions import GardenSystemError, GardenUserError
from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.tasks import add_garden_location, lookup_plant_by_name
from encouragemint.encouragemint.tests.helpers import SAMPLE_GARDEN, SAMPLE_PLANT, create_test_garden
from encouragemint.interfaces.trefle.exceptions import TrefleConnectionError


class TestAddGardenLocation(TestCase):
    def setUp(self):
        self.garden_data = SAMPLE_GARDEN.copy()

        patcher = patch("encouragemint.encouragemint.tasks.register_garden_coordinates")
        self.mock_register_garden_coordinates = patcher.start()
        self.addCleanup(patcher.stop)

    def test_successful_add_garden_location(self):
        self.mock_register_garden_coordinates.return_value = {}

        task = add_garden_location.s(self.garden_data).apply()

        self.assertEqual("SUCCESS", task.status)

    @patch("encouragemint.encouragemint.tasks.add_garden_location.retry")
    def test_add_garden_location_retries_on_GardenSystemError_raise(self, mock_retry):
        self.mock_register_garden_coordinates.side_effect = error = GardenSystemError(None)
        mock_retry.side_effect = Retry

        self.assertRaises(Retry, add_garden_location, self.garden_data)
        mock_retry.assert_called_with(countdown=ANY, exc=error)

    def test_add_garden_location_raises_GardenUserError(self):
        self.mock_register_garden_coordinates.side_effect = GardenUserError(None)

        self.assertRaises(GardenUserError, add_garden_location, self.garden_data)


class TestLookupPlantByName(TestCase):
    def setUp(self):
        patcher = patch("encouragemint.encouragemint.tasks.lookup_plants")
        self.mock_trefle = patcher.start()
        self.addCleanup(patcher.stop)
        test_garden_id = create_test_garden()["garden_id"]
        self.test_garden = Garden.objects.get(garden_id=test_garden_id)

    def test_successful_create_plant(self):
        test_plant = SAMPLE_PLANT.copy()
        self.mock_trefle.return_value = test_plant

        response = lookup_plant_by_name("common_name", "Barflower", self.test_garden)

        self.assertEqual(test_plant.get("scientific_name"), response.get("scientific_name"))
        self.assertEqual(test_plant.get("common_name"), response.get("common_name"))
        self.assertEqual(test_plant.get("duration"), response.get("duration"))
        self.assertEqual(test_plant.get("bloom_period"), response.get("bloom_period"))
        self.assertEqual(test_plant.get("growth_period"), response.get("growth_period"))
        self.assertEqual(test_plant.get("growth_rate"), response.get("growth_rate"))
        self.assertEqual(test_plant.get("shade_tolerance"), response.get("shade_tolerance"))
        self.assertEqual(test_plant.get("moisture_use"), response.get("moisture_use"))
        self.assertEqual(
            test_plant.get("family_common_name"), response.get("family_common_name"))
        self.assertEqual(self.test_garden.garden_id, response.get("garden"))
        self.assertEqual(test_plant.get("trefle_id"), response.get("trefle_id"))

    def test_unsuccessful_from_trefle_exception(self):
        self.mock_trefle.side_effect = TrefleConnectionError

        self.assertRaises(TrefleConnectionError, lookup_plant_by_name, "common_name", "Barflower", self.test_garden)

    def test_successful_with_many_trefle_results(self):
        test_responses_dir = "encouragemint/interfaces/trefle/tests/test_responses"
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            search_many_matches = json.load(file)
        self.mock_trefle.return_value = search_many_matches

        response = lookup_plant_by_name("common_name", "Barflower", self.test_garden)

        self.assertEquals(search_many_matches, response)

    def test_unsuccessful_from_no_trefle_results(self):
        self.mock_trefle.return_value = []

        response = lookup_plant_by_name("common_name", "Barflower", self.test_garden)

        self.assertEquals([], response)
