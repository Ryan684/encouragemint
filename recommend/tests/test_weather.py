import json
from unittest.mock import patch

from django.test import TestCase

from backend.interfaces.meteostat.exceptions import MeteostatConnectionError
from recommend import weather


class TestGetGardenMoisture(TestCase):
    def setUp(self):
        test_responses_dir = "backend/tests/unit_tests/test_responses"
        with open(f"{test_responses_dir}/search_for_nearest_weather_stations.json", "r") as file:
            self.station_search_with_data = json.load(file)
        with open(f"{test_responses_dir}/get_station_weather_record.json", "r") as file:
            self.weather_record_with_data = json.load(file)

        patcher = patch("recommend.weather.search_for_nearest_weather_stations")
        self.search_for_nearest_weather_stations = patcher.start()

        patcher = patch("recommend.weather.get_station_weather_record")
        self.get_station_weather_record = patcher.start()

        self.addCleanup(patcher.stop)

    def test_successful_get_garden_moisture_with_data(self):
        self.search_for_nearest_weather_stations.return_value = self.station_search_with_data
        self.get_station_weather_record.return_value = self.weather_record_with_data

        moisture = weather.get_garden_moisture(123456, 789010, "SPRING")

        self.assertEqual("High", moisture)

    def test_successful_get_garden_moisture_with_data_in_earlier_year_only(self):
        mocked_weather_records = [
            [], [], self.weather_record_with_data
        ]
        self.search_for_nearest_weather_stations.return_value = \
            self.station_search_with_data
        self.get_station_weather_record.side_effect = mocked_weather_records

        moisture = weather.get_garden_moisture(123456, 789010, "SPRING")

        self.assertEqual("High", moisture)

    def test_successful_get_garden_moisture_with_no_historical_data(self):
        self.search_for_nearest_weather_stations.return_value = \
            self.station_search_with_data
        self.get_station_weather_record.return_value = []

        moisture = weather.get_garden_moisture(123456, 789010, "SPRING")

        self.assertIsNone(moisture)

    def test_unsuccessful_get_garden_moisture_from_station_search_meteostat_exception(self):
        self.search_for_nearest_weather_stations.side_effect = \
            MeteostatConnectionError

        moisture = weather.get_garden_moisture(123456, 789010, "SPRING")

        self.assertIsNone(moisture)

    def test_unsuccessful_get_garden_moisture_from_weather_search_meteostat_exception(self):
        self.search_for_nearest_weather_stations.return_value = \
            self.station_search_with_data
        self.get_station_weather_record.side_effect = MeteostatConnectionError

        moisture = weather.get_garden_moisture(123456, 789010, "SPRING")

        self.assertIsNone(moisture)

    def test_unsuccessful_get_garden_moisture_from_no_station_data(self):
        self.search_for_nearest_weather_stations.return_value = []

        moisture = weather.get_garden_moisture(123456, 789010, "SPRING")

        self.assertIsNone(moisture)

    def test_unsuccessful_get_garden_moisture_from_no_historical_weather_data(self):
        self.search_for_nearest_weather_stations.return_value = \
            self.station_search_with_data
        self.get_station_weather_record.return_value = []

        moisture = weather.get_garden_moisture(123456, 789010, "SPRING")

        self.assertIsNone(moisture)