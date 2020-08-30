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

    def test_invalid_duration_parameter(self):
        request = self.factory.post(
            self.recommend_url,
            {"season": "summer", "duration": "yearly"},
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": "The duration must be one of the following: ['PERENNIAL', 'ANNUAL', 'BIENNIAL']"
            },
            response.data
        )

    def test_invalid_bloom_period_parameter(self):
        allowed_bloom_periods = ["EARLY SPRING", "MID SPRING", "SPRING", "LATE SPRING"]
        request = self.factory.post(
            self.recommend_url,
            {"season": "spring", "bloom_period": "march"},
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": f"The bloom_period must be one of the following: {allowed_bloom_periods}"
            },
            response.data
        )
