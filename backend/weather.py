import logging

from backend import seasons
from backend.interfaces.meteostat.meteostat import get_location_weather_data

logger = logging.getLogger("django")


def get_garden_moisture(latitude, longitude, season):
    average_rainfall = _get_average_rainfall_for_season(latitude, longitude, season)

    if average_rainfall:
        if average_rainfall > 60:
            moisture_use = "High"
        elif 30 < average_rainfall < 60:
            moisture_use = "Medium"
        else:
            moisture_use = "Low"
        return moisture_use

    return None


def _get_average_rainfall_for_season(latitude, longitude, season):
    weather_data = get_location_weather_data(latitude, longitude)

    if weather_data:
        rainfall_records = []
        for weather_record in weather_data:
            _append_rainfall_for_month(rainfall_records, season, weather_record)

        if rainfall_records:
            return sum(rainfall_records) / len(rainfall_records)

    return None


def _append_rainfall_for_month(rainfall_records, season, weather_record):
    if weather_record.get("month") in _get_months_numbers(season):
        if weather_record.get("prcp"):
            rainfall_records.append(weather_record["prcp"])


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
