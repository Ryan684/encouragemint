from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from recommend.views import recommend


class TestRecommend(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = recommend
        self.recommend_url = "/recommend/"

    def test_missing_season_parameter(self):
        request = self.factory.post(
            self.recommend_url,
            {},
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": "You must specify a season query parameter for plant recommendations."},
            response.data
        )

    def test_invalid_season_parameter(self):
        request = self.factory.post(
            self.recommend_url,
            {"season": "december"},
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": "The season must be one of the following: ['SPRING', "
                           "'SUMMER', 'AUTUMN', 'WINTER']"
            },
            response.data
        )
