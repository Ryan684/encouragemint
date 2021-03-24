import json
from unittest.mock import patch

from django.test import TestCase

from backend.recommender import recommend_plants


class TestRecommendPlants(TestCase):
    def setUp(self):
        test_responses_dir = "backend/tests/unit_tests/interfaces/trefle/test_responses"
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            self.recommend_many_results = json.load(file)
        with open(f"{test_responses_dir}/plant_search_one_match.json", "r") as file:
            self.recommend_one_result = json.load(file)

        weather_patcher = patch(
            "backend.recommender.get_garden_moisture", return_value="Medium")
        self.mock_weather = weather_patcher.start()
        garden_locator_patcher = patch(
            "backend.recommender.get_coordinates", return_value=(12345, 678910))
        self.mock_weather = garden_locator_patcher.start()
        trefle_patcher = patch("backend.recommender.lookup_plants")
        self.mock_trefle = trefle_patcher.start()

        self.addCleanup(weather_patcher.stop)
        self.addCleanup(garden_locator_patcher.stop)
        self.addCleanup(trefle_patcher.stop)

        self.base_input_data = {
            "bloom_period": "SUMMER",
            "direction": "NORTH",
            "location": "Romsey, UK",
            "duration": "Annual"
        }

        self.base_expected_trefle_payload = {
            "bloom_period": "Summer",
            "shade_tolerance": "Tolerant",
            "moisture_use": "Medium",
            "duration": "Annual"
        }

    def test_many_one_results(self):
        self.mock_trefle.return_value = self.recommend_one_result

        plants = recommend_plants(self.base_input_data)

        self.mock_trefle.assert_called_with(self.base_expected_trefle_payload)
        self.assertEqual(self.recommend_one_result, plants)

    def test_many_trefle_results(self):
        self.mock_trefle.return_value = self.recommend_many_results

        plants = recommend_plants(self.base_input_data)

        self.mock_trefle.assert_called_with(self.base_expected_trefle_payload)
        self.assertEqual(self.recommend_many_results, plants)
