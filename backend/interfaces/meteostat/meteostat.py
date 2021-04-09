import requests
from django.conf import settings

METEOSTAT_URL = "https://api.meteostat.net/v2/"
CLIMATE_NORMALS_ENDPOINT = METEOSTAT_URL + "point/climate"
HEADERS = {"content-type": "application/json", "x-api-key": settings.METEOSTAT_API_KEY}
DATA_KEY = "data"


def get_location_weather_data(latitude, longitude):
    stations = requests.get(
        url=CLIMATE_NORMALS_ENDPOINT,
        headers=HEADERS,
        params={
            "lat": latitude,
            "lon": longitude
        }
    ).json()

    return stations.get(DATA_KEY)
