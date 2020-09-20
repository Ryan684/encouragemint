import json
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from recommend.interfaces.meteostat.exceptions import MeteostatConnectionError
from recommend.interfaces.trefle.exceptions import TrefleConnectionError
from recommend.exceptions import GeocoderNoResultsError
from recommend.views import RecommendView


class TestRecommendView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RecommendView.as_view()
        self.recommend_url = "/recommend/"
        self.valid_payload = {"season": "summer", "direction": "South", "location": "Romsey, UK"}

    def test_missing_mandatory_parameters(self):
        payload = {"season": "summer", "direction": "South"}

        response = self._post_to_endpoint(payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            str("{'location': [ErrorDetail(string='This field is required.', code='required')]}"),
            str(response.data)
        )

    @patch("recommend.views.recommend_plants")
    def test_trefle_connection_error(self, mock_recommendations):
        mock_recommendations.side_effect = TrefleConnectionError

        response = self._post_to_endpoint(self.valid_payload)

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        self.assertEqual(
            {"message": "We're unable to recommend plants for you right now, try again later."},
            response.data
        )

    @patch("recommend.views.recommend_plants")
    def test_meteostat_connection_error(self, mock_recommendations):
        mock_recommendations.side_effect = MeteostatConnectionError

        response = self._post_to_endpoint(self.valid_payload)

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        self.assertEqual(
            {"message": "We're unable to recommend plants for you right now, try again later."},
            response.data
        )

    @patch("recommend.views.recommend_plants")
    def test_geocoder_no_results_error(self, mock_recommendations):
        mock_recommendations.side_effect = GeocoderNoResultsError

        response = self._post_to_endpoint(self.valid_payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {"message": "We couldn't find your location. Please try and be more specific."},
            response.data
        )

    @patch("recommend.views.recommend_plants")
    def test_valid_task_call(self, mock_recommendations):
        with open("recommend/interfaces/trefle/tests/test_responses/plant_search_one_match.json", "r") as file:
            recommend_one_result = json.load(file)
        mock_recommendations.return_value = recommend_one_result

        response = self._post_to_endpoint(self.valid_payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(recommend_one_result, response.data)

    def _post_to_endpoint(self, payload):
        request = self.factory.post(self.recommend_url, payload, format="json")
        response = self.view(request)
        response.render()

        return response
