from django.test import TestCase
from django.urls import resolve


class TestUrlRouting(TestCase):
    def test_recommend_url(self):
        viewset = resolve("/recommend/")
        self.assertEqual(viewset.func.__name__, "RecommendView")


