import json
from unittest.mock import patch

from django.test import TestCase

from backend import seasons
from backend.recommender import recommend_plants


class TestRecommendPlants(TestCase):
    def setUp(self):
        test_responses_dir = "backend/tests/unit_tests/interfaces/trefle/test_responses"
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            self.recommend_many_results = json.load(file)
        self.mock_coordinates = (12345, 678910)
        self.mock_temperatures = (11.1, 15.22)

        weather_patcher = patch("backend.recommender.get_garden_temperature")
        self.mock_weather = weather_patcher.start()
        garden_locator_patcher = patch(
            "backend.recommender.get_coordinates", return_value=self.mock_coordinates)
        self.mock_garden_locator = garden_locator_patcher.start()
        trefle_patcher = patch("backend.recommender.lookup_plants", return_value=self.recommend_many_results)
        self.mock_trefle = trefle_patcher.start()

        self.addCleanup(weather_patcher.stop)
        self.addCleanup(garden_locator_patcher.stop)
        self.addCleanup(trefle_patcher.stop)

    def test_without_both_temperature_parameters(self):
        self.mock_weather.return_value = None, None
        expected_trefle_payload = self._get_trefle_payload()
        expected_trefle_payload.pop("minimum_temperature_deg_c")
        expected_trefle_payload.pop("maximum_temperature_deg_c")

        self._assert_recommendation(expected_trefle_payload)

    def test_without_one_temperature_parameters(self):
        self.mock_weather.return_value = None, self.mock_temperatures[1]
        expected_trefle_payload = self._get_trefle_payload()
        expected_trefle_payload.pop("minimum_temperature_deg_c")

        self._assert_recommendation(expected_trefle_payload)

    def test_with_temperature_parameters(self):
        self.mock_weather.return_value = self.mock_temperatures[0], self.mock_temperatures[1]
        expected_trefle_payload = self._get_trefle_payload()

        self._assert_recommendation(expected_trefle_payload)

    def _assert_recommendation(self, expected_trefle_payload):
        input_data = {
            "bloom_period": seasons.EARLY_SUMMER,
            "location": "Romsey, UK",
            "duration": "Annual"
        }

        plants = recommend_plants(input_data)

        self.mock_garden_locator.assert_called_once_with(input_data["location"])
        self.mock_weather.assert_called_once_with(
            self.mock_coordinates[0], self.mock_coordinates[1], input_data["bloom_period"])
        self.mock_trefle.assert_called_once_with(expected_trefle_payload)
        self.assertEqual(self.recommend_many_results, plants)

    def _get_trefle_payload(self):
        return {
            "bloom_months": seasons.BLOOM_MONTHS[seasons.EARLY_SUMMER],
            "duration": "Annual",
            "minimum_temperature_deg_c": self.mock_temperatures[0],
            "maximum_temperature_deg_c": self.mock_temperatures[1]
        }
