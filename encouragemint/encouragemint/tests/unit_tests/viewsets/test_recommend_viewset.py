import json
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.tests.unit_tests.viewsets.helpers import create_test_garden
from encouragemint.encouragemint.views import RecommendViewSet
from encouragemint.lib.trefle.exceptions import TrefleConnectionError

RECOMMEND_URL = "/recommend/"
SAMPLE_GARDEN = create_test_garden()
GARDEN_ID = SAMPLE_GARDEN.get("garden_id")


class TestRecommendViewsetParameters(TestCase):
    def test_viewset_parameters(self):
        self.assertEqual(["get"], RecommendViewSet.http_method_names)
        self.assertEqual("garden_id", RecommendViewSet.lookup_field)

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RecommendViewSet.as_view()

        test_responses_dir = "encouragemint/lib/trefle/tests/test_responses"
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            self.recommend_many_results = json.load(file)

        weather_patcher = patch(
            "encouragemint.encouragemint.views.get_garden_moisture", return_value="Medium")
        self.mock_weather = weather_patcher.start()
        self.addCleanup(weather_patcher.stop)

        trefle_patcher = patch("encouragemint.encouragemint.views.TREFLE.lookup_plants")
        self.mock_trefle = trefle_patcher.start()
        self.addCleanup(trefle_patcher.stop)

    def test_unsuccessful_recommendation_from_no_season_parameter(self):
        request = self.factory.get(RECOMMEND_URL, format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "Message": "You must specify a season url parameter for plant recommendations."
            },
            response.data
        )

    def test_unsuccessful_recommendation_from_invalid_season_parameter(self):
        request = self.factory.get(f"{RECOMMEND_URL}/?season=december", format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "Message": "The season must be either Spring, Summer, Autumn or Winter."
            },
            response.data
        )

    def test_successful_recommendation(self):
        self.mock_trefle.return_value = self.recommend_many_results

        request = self.factory.get(f"{RECOMMEND_URL}/?season=spring", format="json")
        response = self.view(request, garden_id=GARDEN_ID)
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

        request = self.factory.get(f"{RECOMMEND_URL}/?season=spring", format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(recommend_single_result, model_data)

    def test_successful_recommendation_but_no_results(self):
        self.mock_trefle.return_value = []

        request = self.factory.get(f"{RECOMMEND_URL}/?season=spring", format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], model_data)

    def test_successful_recommendation_but_no_meteostat_data(self):
        self.mock_trefle.return_value = self.recommend_many_results
        self.mock_weather.return_value = None

        request = self.factory.get(f"{RECOMMEND_URL}/?season=spring", format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.recommend_many_results, model_data)

    def test_unsuccessful_recommendation_from_trefle_exception(self):
        self.mock_trefle.side_effect = TrefleConnectionError

        request = self.factory.get(f"{RECOMMEND_URL}/?season=spring", format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        self.assertEqual(
            {
                "Message": "Encouragemint can't recommend plants for your garden right now. "
                           "Try again later."
            },
            response.data
        )
