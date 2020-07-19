from unittest.mock import patch

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from backend.src.views.login_view import login
from backend.tests.helpers import generate_new_user_payload


class TestPlantDetailView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = login
        self.login_url = "/login/"

    def test_unsuccessful_request_from_no_username_parameter(self):
        request = self.factory.post(
            self.login_url,
            {"password": "foo"},
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": "You must specify a username parameter to login."
            },
            response.data
        )

    def test_unsuccessful_request_from_no_password_parameter(self):
        request = self.factory.post(
            self.login_url,
            {"username": "foo"},
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": "You must specify a password parameter to login."
            },
            response.data
        )

    def test_unsuccessful_request_from_non_existent_user_login(self):
        request = self.factory.post(
            self.login_url,
            {
                "username": "Foobar",
                "password": "Whizzbang"
            },
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({"message": "login failed"}, response.data)

    @patch("backend.src.views.login_view.authenticate")
    def test_successful_login(self, mocked_authenticate):
        mocked_authenticate.return_value = True
        payload = generate_new_user_payload()
        user = User.objects.create(**payload)

        request = self.factory.post(
            self.login_url,
            {
                "username": user.username,
                "password": user.password
            },
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({"message": "login successful"}, response.data)
