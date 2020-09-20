from django.test import TestCase
from django.urls import resolve


class TestUrlRouting(TestCase):
    def test_user_url(self):
        viewset = resolve("/user/")
        self.assertEqual(viewset.func.__name__, "UserViewSet")

    def test_garden_url(self):
        viewset = resolve("/garden/")
        self.assertEqual(viewset.func.__name__, "GardenViewSet")

    def test_plant_url(self):
        viewset = resolve("/plant/")
        self.assertEqual(viewset.func.__name__, "PlantViewSet")

    def test_plant_detail_url(self):
        arbitrary_trefle_id = "123456"
        viewset = resolve(f"/plant_detail/{arbitrary_trefle_id}/")
        self.assertEqual(viewset.func.__name__, "plant_detail")

    def test_login_url(self):
        viewset = resolve(f"/login/")
        self.assertEqual(viewset.func.__name__, "login")
