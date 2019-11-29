from requests import get


class TrefleAPI:
    PLANTS_ENDPOINT = "http://trefle.io/api/plants/"
    HEADERS = {"content-type": "application/json"}
    TOKEN = "aUF2TXNmazZhbENpTCtJWkhqTUIvUT09"

    def lookup_plant(self, plant_name):
        results = self._send_trefle_request(
            self._compile_parameters("common_name", plant_name),
            self._compile_url()
        ).json()
        if len(results) == 1:
            plant = self._send_trefle_request(
                self._compile_parameters(),
                self._compile_url(results[0].get("id"))
            ).json()
            return self._extract_plant_data(plant)
        return results

    def _compile_parameters(self, key=None, value=None):
        params = {
            "token": self.TOKEN
        }
        if key and value:
            params[key] = value
        return params

    def _compile_url(self, plant_id=None):
        url = self.PLANTS_ENDPOINT
        if plant_id:
            url = url + str(plant_id)
        return url

    def _send_trefle_request(self, parameters, url):
        response = get(
            url=url,
            headers=self.HEADERS,
            params=parameters,
            verify=False
        )
        return response

    def _extract_plant_data(self, plant):
        # TEMP
        return {
            "trefle_id": 134845,
            "scientific_name": "Eriophyllum lanatum",
            "duration": "Annual, Perennial",
            "bloom_period": None,
            "growth_period": None,
            "growth_rate": None,
            "shade_tolerance": None,
            "moisture_use": None,
            "family_common_name": "Aster family"
        }
