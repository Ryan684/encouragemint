import requests
from django.conf import settings

from encouragemint.lib.trefle.exceptions import TrefleConnectionError


class TrefleAPI:
    TREFLE_URL = "http://trefle.io/api/plants/"
    HEADERS = {"content-type": "application/json"}
    TOKEN = settings.TREFLE_API_KEY

    def lookup_plants(self, trefle_query):
        try:
            results = self._lookup_plants_by_name(trefle_query)

            if len(results) == 1:
                plant = self._lookup_plant_by_id(results[0].get("id"))
                return self._extract_plant_data(plant)

            return results
        except requests.RequestException:
            raise TrefleConnectionError()

    def _lookup_plants_by_name(self, trefle_query):
        results = self._send_trefle_request(
            self._compile_parameters(trefle_query),
            self._compile_url()
        )

        if isinstance(results, list):
            return results

        return results.json()

    def _lookup_plant_by_id(self, plant_id):
        return self._send_trefle_request(
            self._compile_parameters(),
            self._compile_url(plant_id)
        ).json()

    def _compile_parameters(self, extra_parameters=None):
        url_parameters = {
            "token": self.TOKEN,
            "page_size": 100
        }

        if extra_parameters:
            for parameter in extra_parameters:
                url_parameters[parameter] = extra_parameters[parameter]

        return url_parameters

    def _compile_url(self, plant_id=None):
        url = self.TREFLE_URL

        if plant_id:
            url = url + str(plant_id)

        return url

    def _send_trefle_request(self, parameters, url):
        return requests.get(
            url=url,
            headers=self.HEADERS,
            params=parameters
        )

    def _extract_plant_data(self, plant):  # pylint: disable=no-self-use
        return {
            "trefle_id": plant.get("id"),
            "common_name": plant.get("common_name"),
            "duration": plant.get("duration"),
            "bloom_period": plant.get("main_species").get("seed").get("bloom_period"),
            "growth_period": plant.get("main_species").get("specifications").get("growth_period"),
            "growth_rate": plant.get("main_species").get("specifications").get("growth_rate"),
            "shade_tolerance": plant.get("main_species").get("growth").get("shade_tolerance"),
            "moisture_use": plant.get("main_species").get("growth").get("moisture_use"),
            "scientific_name": plant.get("scientific_name"),
            "family_common_name": plant.get("family_common_name"),
        }
