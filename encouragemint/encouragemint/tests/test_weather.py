import json
from unittest.mock import patch

from django.test import TestCase

from encouragemint.encouragemint import weather
from encouragemint.encouragemint.models import Garden
from encouragemint.encouragemint.tests.viewsets.helpers import create_test_garden


class TestWeatherFunctions(TestCase):
    def setUp(self):
        self.test_garden = Garden.objects.get(garden_id=create_test_garden().get("garden_id"))
        with open("encouragemint/encouragemint/tests/test_responses/search_for_nearest_weather_stations_with_data.json", "r") as file:
            self.station_search_with_data = json.load(file)
        with open("encouragemint/encouragemint/tests/test_responses/get_station_weather_record_with_data.json", "r") as file:
            self.weather_record_with_data = json.load(file)
        patcher = patch("encouragemint.encouragemint.weather.METEOSTAT")
        self.mock_meteostat = patcher.start()
        self.addCleanup(patcher.stop)

    def test_successful_get_garden_moisture_with_data(self):
        self.mock_meteostat.search_for_nearest_weather_stations.return_value = self.station_search_with_data
        self.mock_meteostat.get_station_weather_record.return_value = self.weather_record_with_data

        moisture = weather.get_garden_moisture(self.test_garden)

        self.assertEquals(moisture, "High")

    def test_successful_get_garden_moisture_with_data_in_earlier_year_only(self):
        # mock_meteostat.search_for_nearest_weather_stations.return_value = self.station_search_with_data
        # mock_meteostat.get_station_weather_record.return_value = self.weather_record_with_data
        #
        # moisture = weather.get_garden_moisture(self.test_garden)
        # self.assertEquals(moisture, "Medium")
        pass

    def test_successful_get_garden_moisture_with_no_historical_data(self):
        self.mock_meteostat.search_for_nearest_weather_stations.return_value = self.station_search_with_data
        self.mock_meteostat.get_station_weather_record.return_value = []

        moisture = weather.get_garden_moisture(self.test_garden)

        self.assertIsNone(moisture)

    def test_unsuccessful_get_garden_moisture_from_meteostat_exception(self):
        pass

    def test_unsuccessful_get_garden_moisture_from_no_station_data(self):
        pass

    def test_unsuccessful_get_garden_moisture_from_no_historical_weather_data(self):
        pass