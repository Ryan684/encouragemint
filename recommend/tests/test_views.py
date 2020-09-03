from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from recommend.views import RecommendView


class TestRecommend(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = RecommendView.as_view()
        self.recommend_url = "/recommend/"

    def test_missing_mandatory_parameters(self):
        request = self.factory.post(
            self.recommend_url,
            {"season": "summer", "direction": "South"},
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            str("{'location': [ErrorDetail(string='This field is required.', code='required')]}"),
            str(response.data)
        )

    @patch("recommend.views.execute_recommendation")
    def test_valid_task_call(self, mock_task_call):
        mock_task_call.return_value = {}

        request = self.factory.post(
            self.recommend_url,
            {"season": "summer", "direction": "South", "location": "Romsey, UK"},
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)
        self.assertEqual({"Processing.."}, response.data)
