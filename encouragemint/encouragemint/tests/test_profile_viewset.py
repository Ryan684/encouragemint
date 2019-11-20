import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.views import ProfileViewSet

PROFILE_URL = "/profile/"


class TestPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileViewSet.as_view({"post": "create"})

    def test_create_profile(self):
        payload = {"first_name": "Foo", "last_name": "Bar"}
        request = self.factory.post(PROFILE_URL, payload, format="json")
        response = self.view(request)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))
        self.assertIn("profile_id", model_data)
        self.assertEqual("Foo", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))

    def test_invalid_first_name(self):
        payload = {"first_name": "F00", "last_name": "Bar"}
        request = self.factory.post(PROFILE_URL, payload, format="json")
        response = self.view(request)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        response.render()
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"first_name": ["Your first name can only contain letters."]}
        )

    def test_invalid_last_name(self):
        payload = {"first_name": "Foo", "last_name": "B4r"}
        request = self.factory.post(PROFILE_URL, payload, format="json")
        response = self.view(request)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        response.render()
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"last_name": ["Your last name can only contain letters."]}
        )
