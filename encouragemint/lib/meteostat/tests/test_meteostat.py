import json
from unittest.mock import patch, Mock

import requests
from django.test import override_settings, TestCase

from encouragemint.lib.meteostat.exceptions import MeteostatConnectionError
from encouragemint.lib.meteostat.meteostat import MeteostatAPI


@override_settings(METEOSTAT_API_KEY="Foo")
class TestMeteostat(TestCase):
    def setUp(self):
        self.meteostat = MeteostatAPI()
        self.sample_latitude = 50.98893
        self.sample_longitude = -1.49658
        self.sample_weather_station = "03865"
        self.sample_weather_start_date = "2019-01"
        self.sample_weather_end_date = "2019-12"

        with open("encouragemint/lib/meteostat/tests/test_responses/station_search_response_no_data.json", "r") as file:
            self.station_search_matches = json.load(file)
        with open("encouragemint/lib/meteostat/tests/test_responses/station_search_response_with_data.json", "r") as file:
            self.station_search_no_matches = json.load(file)
        with open("encouragemint/lib/meteostat/tests/test_responses/station_weather_lookup_with_data.json", "r") as file:
            self.station_weather_data = json.load(file)
        with open("encouragemint/lib/meteostat/tests/test_responses/station_weather_lookup_no_data.json", "r") as file:
            self.station_weather_no_data = json.load(file)

        patcher = patch("requests.post")
        self.mock_post = patcher.start()
        self.addCleanup(patcher.stop)

    def test_successful_search_for_nearest_weather_stations(self):
        mock = Mock()
        mock.json.return_value = self.station_search_matches
        self.mock_post.return_value = mock

        stations = self.meteostat.search_for_nearest_weather_stations(self.sample_latitude, self.sample_longitude)
        
        self.assertEquals(self.station_search_matches.get("data"), stations)

    def test_unsuccessful_search_for_nearest_weather_stations(self):
        mock = Mock()
        mock.json.return_value = self.station_search_no_matches
        self.mock_post.return_value = mock

        stations = self.meteostat.search_for_nearest_weather_stations(self.sample_latitude, self.sample_longitude)

        self.assertEquals(self.station_search_no_matches.get("data"), stations)

    def test_unsuccessful_search_for_nearest_weather_stations_from_meteostat_exception(self):
        self.mock_post.side_effect = requests.exceptions.ConnectionError

        self.assertRaises(
            MeteostatConnectionError,
            self.meteostat.search_for_nearest_weather_stations,
            self.sample_latitude,
            self.sample_longitude
        )

    def test_successful_get_station_weather_record(self):
        mock = Mock()
        mock.json.return_value = self.station_weather_data
        self.mock_post.return_value = mock

        weather_report = self.meteostat.get_station_weather_record(
            self.sample_weather_start_date,
            self.sample_weather_end_date,
            self.sample_weather_station
        )

        self.assertEquals(self.station_weather_data.get("data"), weather_report)

    def test_unsuccessful_get_station_weather_record(self):
        mock = Mock()
        mock.json.return_value = self.station_weather_no_data
        self.mock_post.return_value = mock

        weather_report = self.meteostat.get_station_weather_record(
            self.sample_weather_start_date,
            self.sample_weather_end_date,
            self.sample_weather_station
        )

        self.assertEquals(self.station_weather_no_data.get("data"), weather_report)

    def test_unsuccessful_get_station_weather_record_from_meteostat_exception(self):
        self.mock_post.side_effect = requests.exceptions.ConnectionError

        self.assertRaises(
            MeteostatConnectionError,
            self.meteostat.get_station_weather_record,
            self.sample_weather_start_date,
            self.sample_weather_end_date,
            self.sample_weather_station
        )