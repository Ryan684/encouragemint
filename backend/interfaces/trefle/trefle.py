import requests
from django.conf import settings

from backend.interfaces.trefle.exceptions import TrefleConnectionError


TREFLE_URL = "http://trefle.io/api/v1"
PLANTS_ENDPOINT = f"{TREFLE_URL}/plants/"
HEADERS = {"content-type": "application/json"}
TOKEN = settings.TREFLE_API_KEY


def lookup_plants(search_parameters):
    try:
        return requests.get(
            url=PLANTS_ENDPOINT,
            headers=HEADERS,
            params=_compile_parameters(search_parameters)
        ).json()
    except requests.RequestException as exception:
        raise TrefleConnectionError(exception)


def _compile_parameters(search_parameters):
    url_parameters = {
        "token": TOKEN,
        "page_size": 100
    }

    for parameter in search_parameters:
        url_parameters[f"filter[{parameter}]"] = search_parameters[parameter]

    return url_parameters
