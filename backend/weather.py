import datetime
import logging

from backend import seasons
from backend.interfaces.meteostat.exceptions import MeteostatConnectionError
from backend.interfaces.meteostat.meteostat import \
    search_for_nearest_weather_stations, get_station_weather_record

logger = logging.getLogger("django")


def get_garden_moisture(latitude, longitude, season):
    try:
        average_rainfall = _get_historical_rainfall_data(latitude, longitude, season)
    except MeteostatConnectionError as exception:
        logger.error(
            "Rainfall data could not be gathered from Meteostat due to "
            f"an error: {exception}")
        return None

    if average_rainfall:
        if average_rainfall > 60:
            moisture_use = "High"
        elif 30 < average_rainfall < 60:
            moisture_use = "Medium"
        else:
            moisture_use = "Low"

        return moisture_use

    return None


def _get_historical_rainfall_data(latitude, longitude, season):
    average_rainfall = None
    this_year = datetime.datetime.now().year
    start_year = this_year - 1
    end_year = start_year

    if seasons.WINTER in season:
        end_year = start_year + 1
        start_month = "12"
        end_month = "02"
    elif seasons.SPRING in season:
        start_month = "03"
        end_month = "05"
    elif seasons.SUMMER in season:
        start_month = "06"
        end_month = "08"
    else:
        start_month = "09"
        end_month = "11"

    while not average_rainfall and start_year != this_year - 5:
        average_rainfall_for_year = _get_average_rainfall_for_season(
            latitude, longitude, f"{start_year}-{start_month}", f"{end_year}-{end_month}")
        if average_rainfall_for_year:
            average_rainfall = average_rainfall_for_year
        else:
            start_year = start_year - 1
            end_year = end_year - 1

    return average_rainfall


def _get_average_rainfall_for_season(latitude, longitude, start_time, end_time):
    nearby_weather_stations = search_for_nearest_weather_stations(latitude, longitude)
    weather_data = None

    for station in nearby_weather_stations:

        station_weather_report = get_station_weather_record(
            start_time, end_time, station.get("id"))

        if station_weather_report:
            weather_data = station_weather_report
            break

    if weather_data:
        rainfall_records = []
        for month in weather_data:
            if month.get("precipitation"):
                rainfall_records.append(month.get("precipitation"))

        if rainfall_records:
            return sum(rainfall_records) / len(rainfall_records)

    return None
