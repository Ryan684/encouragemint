import requests
from django.conf import settings

from encouragemint.interfaces.meteostat.exceptions import MeteostatConnectionError


class MeteostatAPI:
    METEOSTAT_URL = "https://api.meteostat.net/v1/"
    HEADERS = {"content-type": "application/json"}
    TOKEN = settings.METEOSTAT_API_KEY

    def search_for_nearest_weather_stations(self, latitude, longitude):
        parameters = {
            "lat": latitude,
            "lon": longitude,
            "limit": 10,
            "key": self.TOKEN
        }

        try:
            stations = requests.post(
                url=self.METEOSTAT_URL + "stations/nearby",
                headers=self.HEADERS,
                params=parameters
            ).json()

            return stations.get("data")
        except requests.exceptions.RequestException:
            raise MeteostatConnectionError()

    def get_station_weather_record(self, start_date, end_date, station):
        parameters = {
            "start": start_date,
            "end": end_date,
            "station": station,
            "key": self.TOKEN
        }

        try:
            weather_report = requests.post(
                url=self.METEOSTAT_URL + "history/monthly",
                headers=self.HEADERS,
                params=parameters
            ).json()
            return weather_report.get("data")
        except requests.exceptions.RequestException:
            raise MeteostatConnectionError()
