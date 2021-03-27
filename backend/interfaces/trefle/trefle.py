import requests
from django.conf import settings


TREFLE_URL = "http://trefle.io/api/v1"
PLANTS_ENDPOINT = f"{TREFLE_URL}/plants/"
HEADERS = {"content-type": "application/json"}
TOKEN = settings.TREFLE_API_KEY
RANGE_FIELDS = ["minimum_temperature_deg_c", "maximum_temperature_deg_c"]


def lookup_plants(search_parameters):
    return requests.get(
        url=PLANTS_ENDPOINT,
        headers=HEADERS,
        params=_compile_parameters(search_parameters)
    ).json()


def _compile_parameters(search_parameters):
    url_parameters = {
        "token": TOKEN,
        "page_size": 100
    }

    for parameter in search_parameters:
        if parameter in RANGE_FIELDS:
            url_parameters[f"range[{parameter}]"] = search_parameters[parameter]
        else:
            url_parameters[f"filter[{parameter}]"] = search_parameters[parameter]

    return url_parameters
