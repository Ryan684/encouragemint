import requests


class TrefleAPI:
    PLANTS_ENDPOINT = "http://trefle.io/api/plants/"
    HEADERS = {"content-type": "application/json"}
    TOKEN = "aUF2TXNmazZhbENpTCtJWkhqTUIvUT09"

    def lookup_plants_by_scientific_name(self, plant_name):
        return self._lookup_plants("scientific_name", plant_name)

    def lookup_plants_by_wildcarded_name(self, plant_name):
        return self._lookup_plants("q", plant_name)

    def _lookup_plants(self, name_key, plant_name):
        results = self._lookup_plants_by_name(name_key, plant_name)

        if len(results) == 1:
            plant = self._lookup_plant_by_id(results)
            return self._extract_plant_data(plant)

        return results

    def _lookup_plants_by_name(self, name_key, plant_name):
        results = self._send_trefle_request(
            self._compile_parameters(name_key, plant_name),
            self._compile_url()
        )

        if isinstance(results, list):
            return results

        return results.json()

    def _lookup_plant_by_id(self, results):
        return self._send_trefle_request(
            self._compile_parameters(),
            self._compile_url(results[0].get("id"))
        ).json()

    def _compile_parameters(self, key=None, value=None):
        parameters = {
            "token": self.TOKEN
        }

        if key and value:
            parameters[key] = value

        return parameters

    def _compile_url(self, plant_id=None):
        url = self.PLANTS_ENDPOINT

        if plant_id:
            url = url + str(plant_id)

        return url

    def _send_trefle_request(self, parameters, url):
        return requests.get(
            url=url,
            headers=self.HEADERS,
            params=parameters,
            verify=False
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
            "family_common_name": plant.get("family_common_name")
        }