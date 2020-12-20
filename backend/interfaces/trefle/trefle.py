import requests
from django.conf import settings

from backend.interfaces.trefle.exceptions import TrefleConnectionError


TREFLE_URL = "http://trefle.io/api/v1/plants/"
HEADERS = {"content-type": "application/json"}
TOKEN = settings.TREFLE_API_KEY


def lookup_plants(parameters):
    try:
        return requests.get(
            url=TREFLE_URL,
            headers=HEADERS,
            params=_compile_parameters(parameters)
        ).json()
    except requests.RequestException as exception:
        raise TrefleConnectionError(exception)


def _compile_parameters(extra_parameters=None):
    url_parameters = {
        "token": TOKEN,
        "page_size": 100
    }

    if extra_parameters:
        for parameter in extra_parameters:
            url_parameters[parameter] = extra_parameters[parameter]

    return url_parameters
