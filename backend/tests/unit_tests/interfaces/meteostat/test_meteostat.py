import json
from unittest.mock import patch, Mock

from django.test import override_settings, TestCase

from backend.interfaces.meteostat import meteostat


@override_settings(METEOSTAT_API_KEY="Foo")
class TestGetLocationWeatherData(TestCase):
    def setUp(self):
        self.sample_latitude = 50.98893
        self.sample_longitude = -1.49658
        self.test_responses_dir = "tests/unit_tests/interfaces/meteostat/test_responses"

        patcher = patch("requests.get")
        self.mock_get = patcher.start()
        self.addCleanup(patcher.stop)

    def test_weather_data_found(self):
        self._assert_weather_data(f"{self.test_responses_dir}/climate_normals_response.json")

    def test_no_weather_data_found(self):
        self._assert_weather_data(f"{self.test_responses_dir}/climate_normals_response_no_data.json")

    def _assert_weather_data(self, weather_data_response):
        mock = Mock()
        with open(weather_data_response, "r") as file:
            climate_normals = json.load(file)
        mock.json.return_value = climate_normals
        self.mock_get.return_value = mock

        weather_data = meteostat.get_location_weather_data(
                self.sample_latitude, self.sample_longitude)

        self.mock_get.assert_called_once_with(
            url=meteostat.CLIMATE_NORMALS_ENDPOINT,
            headers=meteostat.HEADERS,
            params={
                "lat": self.sample_latitude,
                "lon": self.sample_longitude
            }
        )
        self.assertEqual(climate_normals.get("data"), weather_data)
