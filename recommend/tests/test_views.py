from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from recommend.views import RecommendView


class TestRecommendView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RecommendView.as_view()
        self.recommend_url = "/recommend/"

    def test_missing_mandatory_parameters(self):
        payload = {"season": "summer", "direction": "South"}

        response = self._post_to_endpoint(payload)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            str("{'location': [ErrorDetail(string='This field is required.', code='required')]}"),
            str(response.data)
        )

    @patch("recommend.views.recommend_plants")
    def test_valid_task_call(self, mock_recommendations):
        mock_recommendations.return_value = {}
        payload = {"season": "summer", "direction": "South", "location": "Romsey, UK"}

        response = self._post_to_endpoint(payload)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({}, response.data)

    def _post_to_endpoint(self, payload):
        request = self.factory.post(self.recommend_url, payload, format="json")
        response = self.view(request)
        response.render()

        return response
