import logging

from backend import seasons
from backend.interfaces.meteostat.meteostat import get_location_weather_data

logger = logging.getLogger("django")


def get_garden_temperature(latitude, longitude, season):
    months = _get_months_numbers(season)
    minimum_temperatures = []
    maximum_temperatures = []

    weather_data = get_location_weather_data(latitude, longitude)

    if weather_data:
        for weather_record in weather_data:
            _append_temperature_for_month(minimum_temperatures, months, weather_record, "tmin")
            _append_temperature_for_month(maximum_temperatures, months, weather_record, "tmax")

    return _calculate_average(minimum_temperatures), _calculate_average(maximum_temperatures)


def _get_months_numbers(season):
    if seasons.WINTER in season:
        months = [1, 2, 12]
    elif seasons.SPRING in season:
        months = [3, 4, 5]
    elif seasons.SUMMER in season:
        months = [6, 7, 8]
    else:
        months = [9, 10, 11]
    return months


def _append_temperature_for_month(temperatures, months, weather_record, key):
    if weather_record.get("month") in months:
        if weather_record.get(key):
            temperatures.append(weather_record[key])


def _calculate_average(minimum_temperatures):
    if minimum_temperatures:
        return sum(minimum_temperatures) / len(minimum_temperatures)
