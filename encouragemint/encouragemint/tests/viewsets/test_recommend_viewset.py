import json
from unittest.mock import patch

import requests
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.tests.viewsets.helpers import create_test_garden
from encouragemint.encouragemint.views import RecommendViewSet

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
        with open("encouragemint/lib/trefle/tests/test_responses/plant_search_many_matches.json", "r") as file:
            self.search_many_matches = json.load(file)

        patcher = patch("encouragemint.encouragemint.views.get_garden_moisture", return_value="Medium")
        self.mock_weather = patcher.start()
        self.addCleanup(patcher.stop)

    @patch("requests.get")
    def test_successful_recommendation(self, mock_get):
        mock_get.return_value = self.search_many_matches

        request = self.factory.get(RECOMMEND_URL, format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.search_many_matches, model_data)

    @patch("requests.get")
    def test_successful_recommendation_but_no_results(self, mock_get):
        mock_get.return_value = []

        request = self.factory.get(RECOMMEND_URL, format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], model_data)

    @patch("requests.get")
    def test_successful_recommendation_but_no_meteostat_data(self, mock_get):
        mock_get.return_value = self.search_many_matches
        self.mock_weather.return_value = None

        request = self.factory.get(RECOMMEND_URL, format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(self.search_many_matches, model_data)

    @patch("requests.get")
    def test_unsuccessful_recommendation_from_trefle_exception(self, mock_get):
        mock_get.side_effect = requests.ConnectionError

        request = self.factory.get(RECOMMEND_URL, format="json")
        response = self.view(request, garden_id=GARDEN_ID)
        response.render()

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        self.assertEqual(
            {"Message": "Encouragemint can't recommend plants for your garden right now. Try again later."},
            response.data
        )
