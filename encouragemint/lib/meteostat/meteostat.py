import requests
from django.conf import settings


class MeteostatAPI:
    METEOSTAT_URL = "https://api.meteostat.net/v1/"
    HEADERS = {"content-type": "application/json"}
    TOKEN = settings.METEOSTAT_API_KEY

    # lookup station by long/lat. limit 10 for now
    # for station in stations: if data, return it

    def search_for_nearest_stations(self, latitude, longitude):
        parameters = {
            "lat": latitude,
            "lon": longitude,
            "key": self.TOKEN
        }

        stations = requests.post(
            url=self.METEOSTAT_URL + "stations/nearby",
            headers=self.HEADERS,
            params=parameters
        ).json()

        return stations.get("data")
