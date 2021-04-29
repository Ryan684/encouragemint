import json
from unittest.mock import patch

from django.test import TestCase

from backend import weather, seasons


class TestGetGardenTemperature(TestCase):
    def setUp(self):
        meteostat_responses_dir = "tests/unit_tests/interfaces/meteostat/test_responses"
        with open(f"{meteostat_responses_dir}/climate_normals_response.json", "r") as file:
            self.weather_record_with_data = json.load(file)["data"]
        self.sample_latitude = 123456
        self.sample_longitude = 789010

        patcher = patch("backend.weather.get_location_weather_data")
        self.get_location_weather_data = patcher.start()
        self.addCleanup(patcher.stop)

    def test_weather_data_found_for_location(self):
        self.get_location_weather_data.return_value = self.weather_record_with_data

        moisture = weather.get_garden_temperature(self.sample_latitude, self.sample_longitude, seasons.EARLY_SPRING)

        self.assertEqual((23.133333333333336, 31.233333333333334), moisture)

    def test_no_weather_data_for_location(self):
        self.get_location_weather_data.return_value = []

        moisture = weather.get_garden_temperature(self.sample_latitude, self.sample_longitude, seasons.EARLY_SPRING)

        self.assertEqual((None, None), moisture)

    def test_no_data_for_given_season(self):
        weather_data = self.weather_record_with_data.copy()
        for weather_record in weather_data:
            if weather_record.get("month") in [3, 4, 5]:
                weather_record["tmin"] = None
                weather_record["tmax"] = None
        self.get_location_weather_data.return_value = self.weather_record_with_data

        moisture = weather.get_garden_temperature(self.sample_latitude, self.sample_longitude, seasons.EARLY_SPRING)

        self.assertEqual((None, None), moisture)

    def test_no_data_for_one_temperature_scale_only(self):
        weather_data = self.weather_record_with_data.copy()
        for weather_record in weather_data:
            if weather_record.get("month") in [3, 4, 5]:
                weather_record["tmin"] = None
        self.get_location_weather_data.return_value = self.weather_record_with_data

        moisture = weather.get_garden_temperature(self.sample_latitude, self.sample_longitude, seasons.EARLY_SPRING)

        self.assertEqual((None, 31.233333333333334), moisture)
