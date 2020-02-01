from django.test import TestCase
from django.urls import resolve


class TestUrlRouting(TestCase):
    def test_profile_url(self):
        viewset = resolve("/profile/")
        self.assertEqual(viewset.func.__name__, "ProfileViewSet")

    def test_garden_url(self):
        viewset = resolve("/garden/")
        self.assertEqual(viewset.func.__name__, "GardenViewSet")

    def test_plant_url(self):
        viewset = resolve("/plant/")
        self.assertEqual(viewset.func.__name__, "PlantViewSet")
