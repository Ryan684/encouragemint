from django.conf import settings


class MeteostatAPI:
    METEOSTAT_URL = "https://api.meteostat.net/v1/"
    HEADERS = {"content-type": "application/json"}
    TOKEN = settings.METEOSTAT_API_KEY

    # lookup station by long/lat. limit 10 for now
    # for station in stations: if data, return it
    #
