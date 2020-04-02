import requests
from django.conf import settings

from encouragemint.interfaces.meteostat.exceptions import MeteostatConnectionError


METEOSTAT_URL = "https://api.meteostat.net/v1/"
HEADERS = {"content-type": "application/json"}
TOKEN = settings.METEOSTAT_API_KEY


def search_for_nearest_weather_stations(latitude, longitude):
    parameters = {
        "lat": latitude,
        "lon": longitude,
        "limit": 10,
        "key": TOKEN
    }

    try:
        stations = requests.post(
            url=METEOSTAT_URL + "stations/nearby",
            headers=HEADERS,
            params=parameters
        ).json()

        return stations.get("data")
    except requests.exceptions.RequestException as exception:
        raise MeteostatConnectionError(exception)


def get_station_weather_record(start_date, end_date, station):
    parameters = {
        "start": start_date,
        "end": end_date,
        "station": station,
        "key": TOKEN
    }

    try:
        weather_report = requests.post(
            url=METEOSTAT_URL + "history/monthly",
            headers=HEADERS,
            params=parameters
        ).json()
        return weather_report.get("data")
    except requests.exceptions.RequestException as exception:
        raise MeteostatConnectionError(exception)
