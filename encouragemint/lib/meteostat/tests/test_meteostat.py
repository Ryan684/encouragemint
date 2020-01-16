import json
from unittest.mock import patch, Mock

from django.test import override_settings, TestCase

from encouragemint.lib.meteostat.meteostat import MeteostatAPI


@override_settings(METEOSTAT_API_KEY="Foo")
class TestMeteostat(TestCase):
    def setUp(self):
        self.meteostat = MeteostatAPI()
        self.sample_latitude = 50.98893
        self.sample_longitude = -1.49658
        with open("encouragemint/lib/meteostat/tests/test_responses/station_search_response.json", "r") as file:
            self.station_search_matches = json.load(file)

    @patch("requests.post")
    def test_weather_station_lookup(self, mock_meteostat):
        mock = Mock()
        mock.json.return_value = self.station_search_matches
        mock_meteostat.return_value = mock

        stations = self.meteostat.search_for_nearest_stations(self.sample_latitude, self.sample_longitude)
        
        self.assertEquals(self.station_search_matches.get("data"), stations)
