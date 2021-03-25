import requests
from django.conf import settings

from backend.interfaces.meteostat.exceptions import MeteostatConnectionError


METEOSTAT_URL = "https://api.meteostat.net/v2/"
STATION_SEARCH_ENDPOINT = METEOSTAT_URL + "stations/nearby"
STATION_WEATHER_HISTORY_ENDPOINT = METEOSTAT_URL + "history/monthly"
HEADERS = {"content-type": "application/json", "x-api-key": settings.METEOSTAT_API_KEY}
DATA_KEY = "data"


def search_for_nearest_weather_stations(latitude, longitude):
    try:
        stations = requests.get(
            url=STATION_SEARCH_ENDPOINT,
            headers=HEADERS,
            params={
                "lat": latitude,
                "lon": longitude,
                "limit": 10
            }
        ).json()

        return stations.get(DATA_KEY)
    except requests.exceptions.RequestException as exception:
        raise MeteostatConnectionError(exception)


def get_station_weather_record(start_date, end_date, station):
    try:
        weather_report = requests.get(
            url=STATION_WEATHER_HISTORY_ENDPOINT,
            headers=HEADERS,
            params={
                "start": start_date,
                "end": end_date,
                "station": station
            }
        ).json()
        return weather_report.get(DATA_KEY)
    except requests.exceptions.RequestException as exception:
        raise MeteostatConnectionError(exception)
