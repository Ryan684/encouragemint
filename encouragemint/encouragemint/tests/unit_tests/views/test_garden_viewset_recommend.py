import json
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.tests.helpers import create_test_garden
from encouragemint.encouragemint.views.garden_viewset import GardenViewSet
from encouragemint.interfaces.trefle.exceptions import TrefleConnectionError


class TestGardenViewSetRecommendAction(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GardenViewSet.as_view({"get": "recommend"})

        self.sample_garden = create_test_garden()
        self.garden_id = self.sample_garden.get("garden_id")
        self.recommend_url = f"garden/{self.garden_id}recommend/"

        test_responses_dir = "encouragemint/interfaces/trefle/tests/test_responses"
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            self.recommend_many_results = json.load(file)

        weather_patcher = patch(
            "encouragemint.encouragemint.views.garden_viewset.get_garden_moisture", return_value="Medium")
        self.mock_weather = weather_patcher.start()
        self.addCleanup(weather_patcher.stop)

        trefle_patcher = patch("encouragemint.encouragemint.views.garden_viewset.lookup_plants")
        self.mock_trefle = trefle_patcher.start()
        self.addCleanup(trefle_patcher.stop)

    def test_unsuccessful_recommendation_from_no_season_parameter(self):
        request = self.factory.get(self.recommend_url, format="json")
        response = self.view(request, garden_id=self.garden_id)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": "You must specify a season query parameter for plant recommendations."},
            response.data
        )

    def test_unsuccessful_recommendation_from_invalid_season_parameter(self):
        request = self.factory.get(f"{self.recommend_url}/?season=december", format="json")
        response = self.view(request, garden_id=self.garden_id)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": "The season must be one of the following: ['SPRING', "
                           "'SUMMER', 'AUTUMN', 'WINTER']"
            },
            response.data
        )

    def test_unsuccessful_recommendation_from_invalid_duration_parameter(self):
        request = self.factory.get(f"{self.recommend_url}/?season=Spring&duration=yearly", format="json")
        response = self.view(request, garden_id=self.garden_id)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": "The duration must be one of the following: ['PERENNIAL', 'ANNUAL', 'BIENNIAL']"
            },
            response.data
        )

    def test_unsuccessful_recommendation_from_invalid_bloom_period_parameter(self):
        request = self.factory.get(f"{self.recommend_url}/?season=Spring&bloom_period=Summer", format="json")
        allowed_bloom_periods = ["EARLY SPRING", "MID SPRING", "SPRING", "LATE SPRING"]
        response = self.view(request, garden_id=self.garden_id)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": f"The bloom_period must be one of the following: {allowed_bloom_periods}"
            },
            response.data
        )

    def test_successful_recommendation(self):
        self.mock_trefle.return_value = self.recommend_many_results

        request = self.factory.get(f"{self.recommend_url}/?season=spring", format="json")
        response = self.view(request, garden_id=self.garden_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.recommend_many_results, model_data)

    def test_successful_recommendation_one_result(self):
        recommend_single_result = [
            {
                "slug": "eriophyllum-lanatum",
                "scientific_name": "Eriophyllum lanatum",
                "link": "http://trefle.io/api/plants/134845",
                "id": 134845,
                "complete_data": False,
                "common_name": "common woolly sunflower"
            }
        ]
        self.mock_trefle.return_value = recommend_single_result

        request = self.factory.get(f"{self.recommend_url}/?season=spring", format="json")
        response = self.view(request, garden_id=self.garden_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(recommend_single_result, model_data)

    def test_successful_recommendation_but_no_results(self):
        self.mock_trefle.return_value = []

        request = self.factory.get(f"{self.recommend_url}/?season=spring", format="json")
        response = self.view(request, garden_id=self.garden_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], model_data)

    def test_successful_recommendation_but_no_meteostat_data(self):
        self.mock_trefle.return_value = self.recommend_many_results
        self.mock_weather.return_value = None

        request = self.factory.get(f"{self.recommend_url}/?season=spring", format="json")
        response = self.view(request, garden_id=self.garden_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.recommend_many_results, model_data)

    def test_unsuccessful_recommendation_from_trefle_exception(self):
        self.mock_trefle.side_effect = TrefleConnectionError

        request = self.factory.get(f"{self.recommend_url}/?season=spring", format="json")
        response = self.view(request, garden_id=self.garden_id)
        response.render()

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        self.assertEqual(
            {
                "message": "Encouragemint can't recommend plants for your garden right now. "
                           "Try again later."
            },
            response.data
        )
