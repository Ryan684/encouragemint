import requests
from django.conf import settings

from backend.interfaces.trefle.exceptions import TrefleConnectionError


TREFLE_URL = "http://trefle.io/api/v1"
HEADERS = {"content-type": "application/json"}
TOKEN = settings.TREFLE_API_KEY


def lookup_plants(search_parameters):
    try:
        return requests.get(
            url=f"{TREFLE_URL}/plants/",
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
        url_parameters[parameter] = search_parameters[parameter]

    return url_parameters
