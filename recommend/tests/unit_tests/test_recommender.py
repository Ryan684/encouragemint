import copy
import json
from unittest.mock import patch

from django.test import TestCase

from recommend.recommender import recommend_plants


class TestRecommendPlants(TestCase):
    def setUp(self):
        test_responses_dir = "recommend/interfaces/trefle/tests/test_responses"
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            self.recommend_many_results = json.load(file)
        with open(f"{test_responses_dir}/plant_search_one_match.json", "r") as file:
            self.recommend_one_result = json.load(file)

        weather_patcher = patch(
            "recommend.recommender.get_garden_moisture", return_value="Medium")
        self.mock_weather = weather_patcher.start()
        garden_locator_patcher = patch(
            "recommend.recommender.get_coordinates", return_value=(12345, 678910, "Romsey, UK"))
        self.mock_weather = garden_locator_patcher.start()
        trefle_patcher = patch("recommend.recommender.lookup_plants")
        self.mock_trefle = trefle_patcher.start()

        self.addCleanup(weather_patcher.stop)
        self.addCleanup(garden_locator_patcher.stop)
        self.addCleanup(trefle_patcher.stop)

        self.base_input_data = {
            "season": "SUMMER",
            "direction": "NORTH",
            "location": "Romsey, UK",
        }

        self.base_expected_trefle_payload = {
            "shade_tolerance": "Tolerant",
            "moisture_use": "Medium"
        }

    def test_just_mandatory_parameters(self):
        self.mock_trefle.return_value = self.recommend_one_result

        plants = recommend_plants(self.base_input_data)

        self.mock_trefle.assert_called_with(self.base_expected_trefle_payload)
        self.assertEqual(self.recommend_one_result, plants)

    def test_optional_bloom_period_parameter(self):
        self.mock_trefle.return_value = self.recommend_one_result
        expected_trefle_payload = copy.deepcopy(self.base_expected_trefle_payload)
        expected_trefle_payload["bloom_period"] = "Summer"

        input_data = copy.deepcopy(self.base_input_data)
        input_data["bloom_period"] = "SUMMER"

        plants = recommend_plants(input_data)

        self.mock_trefle.assert_called_with(expected_trefle_payload)
        self.assertEqual(self.recommend_one_result, plants)

    def test_optional_duration_parameter(self):
        self.mock_trefle.return_value = self.recommend_one_result
        expected_trefle_payload = copy.deepcopy(self.base_expected_trefle_payload)
        expected_trefle_payload["duration"] = "Annual"

        input_data = copy.deepcopy(self.base_input_data)
        input_data["duration"] = "Annual"

        plants = recommend_plants(input_data)

        self.mock_trefle.assert_called_with(expected_trefle_payload)
        self.assertEqual(self.recommend_one_result, plants)

    def test_all_parameters(self):
        self.mock_trefle.return_value = self.recommend_one_result
        expected_trefle_payload = copy.deepcopy(self.base_expected_trefle_payload)
        expected_trefle_payload["bloom_period"] = "Summer"
        expected_trefle_payload["duration"] = "Annual"

        input_data = copy.deepcopy(self.base_input_data)
        input_data["bloom_period"] = "SUMMER"
        input_data["duration"] = "Annual"

        plants = recommend_plants(input_data)

        self.assertEqual(self.recommend_one_result, plants)
        self.mock_trefle.assert_called_with(expected_trefle_payload)

    def test_many_trefle_results(self):
        self.mock_trefle.return_value = self.recommend_many_results

        plants = recommend_plants(self.base_input_data)

        self.mock_trefle.assert_called_with(self.base_expected_trefle_payload)
        self.assertEqual(self.recommend_many_results, plants)
