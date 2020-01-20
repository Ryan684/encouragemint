import datetime

from encouragemint.lib.meteostat.meteostat import MeteostatAPI

METEOSTAT = MeteostatAPI()


def get_garden_moisture(garden):
    average_rainfall = _get_historical_rainfall_data(garden)

    if average_rainfall:
        if average_rainfall > 60:
            moisture_use = "High"
        elif 30 < average_rainfall < 60:
            moisture_use = "Medium"
        else:
            moisture_use = "Low"

        return moisture_use

    return None


def _get_historical_rainfall_data(garden):
    this_year = datetime.datetime.now().year
    last_year = this_year - 1
    average_rainfall = None

    while not average_rainfall and last_year != this_year - 5:
        average_rainfall_for_year = _get_average_rainfall(
            garden, f"{last_year}-01", f"{last_year}-12")

        if average_rainfall_for_year:
            average_rainfall = average_rainfall_for_year
        else:
            last_year = last_year - 1

    return average_rainfall


def _get_average_rainfall(garden, start_time, end_time):
    nearby_weather_stations = METEOSTAT.search_for_nearest_weather_stations(
        garden.latitude, garden.longitude)
    weather_data = None

    for station in nearby_weather_stations:
        station_weather_report = METEOSTAT.get_station_weather_record(
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
