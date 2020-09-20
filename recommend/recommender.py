from recommend.interfaces.trefle.trefle import lookup_plants
from recommend.garden_locator import get_coordinates
from recommend.weather import get_garden_moisture


def recommend_plants(serializer_data):
    latitude, longitude, address = get_coordinates(serializer_data["location"])

    query = {"shade_tolerance": _get_required_shade_tolerance(serializer_data["direction"])}
    moisture_use = get_garden_moisture(latitude, longitude, serializer_data["season"])

    if moisture_use:
        query["moisture_use"] = moisture_use

    if serializer_data.get("duration"):
        query["duration"] = serializer_data["duration"].lower().capitalize()

    if serializer_data.get("bloom_period"):
        query["bloom_period"] = serializer_data["bloom_period"].lower().title()

    return lookup_plants(query)


def _get_required_shade_tolerance(direction):
    if direction == "NORTH":
        return "Tolerant"
    if direction == "SOUTH":
        return "Intolerant"
    return "Intermediate"
