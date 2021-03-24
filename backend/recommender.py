from backend.interfaces.trefle.trefle import lookup_plants
from backend.garden_locator import get_coordinates
from backend.weather import get_garden_moisture


def recommend_plants(request_data):
    latitude, longitude = get_coordinates(request_data["location"])

    query = {"shade_tolerance": _get_required_shade_tolerance(request_data["direction"])}
    moisture_use = get_garden_moisture(latitude, longitude, request_data["bloom_period"])

    if moisture_use:
        query["moisture_use"] = moisture_use

    if request_data.get("duration"):
        query["duration"] = request_data["duration"].lower().capitalize()

    if request_data.get("bloom_period"):
        query["bloom_period"] = request_data["bloom_period"].lower().title()

    return lookup_plants(query)


def _get_required_shade_tolerance(direction):
    if direction == "NORTH":
        return "Tolerant"
    if direction == "SOUTH":
        return "Intolerant"
    return "Intermediate"
