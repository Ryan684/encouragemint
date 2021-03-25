import json
from unittest.mock import patch

from django.test import TestCase

from backend.recommender import recommend_plants


class TestRecommendPlants(TestCase):
    def setUp(self):
        test_responses_dir = "backend/tests/unit_tests/interfaces/trefle/test_responses"
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            self.recommend_many_results = json.load(file)
        self.mock_coordinates = (12345, 678910)

        weather_patcher = patch(
            "backend.recommender.get_garden_moisture", return_value="Medium")
        self.mock_weather = weather_patcher.start()
        garden_locator_patcher = patch(
            "backend.recommender.get_coordinates", return_value=self.mock_coordinates)
        self.mock_garden_locator = garden_locator_patcher.start()
        trefle_patcher = patch("backend.recommender.lookup_plants", return_value=self.recommend_many_results)
        self.mock_trefle = trefle_patcher.start()

        self.addCleanup(weather_patcher.stop)
        self.addCleanup(garden_locator_patcher.stop)
        self.addCleanup(trefle_patcher.stop)

    def test_without_moisture_use_parameter(self):
        self.mock_weather.return_value = None
        expected_trefle_payload = self._get_trefle_payload("Tolerant")
        expected_trefle_payload.pop("moisture_use")

        self._assert_recommendation(expected_trefle_payload, "NORTH")

    def test_north_facing_garden(self):
        expected_trefle_payload = self._get_trefle_payload("Tolerant")

        self._assert_recommendation(expected_trefle_payload, "NORTH")

    def test_south_facing_garden(self):
        expected_trefle_payload = self._get_trefle_payload("Intolerant")

        self._assert_recommendation(expected_trefle_payload, "SOUTH")

    def test_other_direction_facing_garden(self):
        expected_trefle_payload = self._get_trefle_payload("Intermediate")

        self._assert_recommendation(expected_trefle_payload, "EAST")

    def _assert_recommendation(self, expected_trefle_payload, garden_direction):
        input_data = {
            "bloom_period": "SUMMER",
            "direction": garden_direction,
            "location": "Romsey, UK",
            "duration": "Annual"
        }

        plants = recommend_plants(input_data)

        self.mock_garden_locator.assert_called_once_with(input_data["location"])
        self.mock_weather.assert_called_once_with(
            self.mock_coordinates[0], self.mock_coordinates[1], input_data["bloom_period"])
        self.mock_trefle.assert_called_once_with(expected_trefle_payload)
        self.assertEqual(self.recommend_many_results, plants)


    @staticmethod
    def _get_trefle_payload(shade_tolerance):
        return {
            "bloom_period": "Summer",
            "shade_tolerance": shade_tolerance,
            "moisture_use": "Medium",
            "duration": "Annual"
        }
