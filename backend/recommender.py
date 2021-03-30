from django.conf import settings

from backend import seasons
from backend.interfaces.trefle.trefle import lookup_plants
from backend.garden_locator import get_coordinates
from backend.weather import get_garden_temperature


def recommend_plants(request_data):
    query = {
        "duration": request_data["duration"].lower().capitalize()
    }

    if settings.WEATHER_DATA_FEATURE_FLAG == "True":
        latitude, longitude = get_coordinates(request_data["location"])
        minimum_temperature, maximum_temperature = get_garden_temperature(
            latitude, longitude, request_data["bloom_period"])

        if minimum_temperature:
            query["minimum_temperature_deg_c"] = f",{minimum_temperature}"

        if maximum_temperature:
            query["maximum_temperature_deg_c"] = maximum_temperature

    if request_data["bloom_period"] != "NO PREFERENCE":
        query["bloom_months"] = seasons.BLOOM_MONTHS[request_data["bloom_period"]]

    return lookup_plants(query)
