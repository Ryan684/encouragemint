from backend import seasons
from backend.interfaces.trefle.trefle import lookup_plants
from backend.garden_locator import get_coordinates
from backend.weather import get_garden_moisture


def recommend_plants(request_data):
    query = {
        "duration": request_data["duration"].lower().capitalize(),
        "bloom_months": seasons.BLOOM_MONTHS[request_data["bloom_period"]]
    }

    latitude, longitude = get_coordinates(request_data["location"])
    moisture_use = get_garden_moisture(latitude, longitude, request_data["bloom_period"])

    if moisture_use:
        query["moisture_use"] = moisture_use

    return lookup_plants(query)
