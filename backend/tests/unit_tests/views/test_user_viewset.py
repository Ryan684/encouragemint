import json

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from backend.src.serializers.user_serializer import UserSerializer
from backend.src.views.user_viewset import UserViewSet
from backend.tests.helpers import create_unique_username, generate_new_user_payload

USER_URL = "/user/"


class TestUserViewsetParameters(TestCase):
    def test_viewset_parameters(self):
        self.assertEqual(
            ["get", "post", "put", "patch", "delete"], UserViewSet.http_method_names)
        self.assertEqual("username", UserViewSet.lookup_field)
        self.assertEqual(UserSerializer, UserViewSet.serializer_class)


class TestDelete(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserViewSet.as_view({"delete": "destroy"})

    def _build_delete_response(self, username):
        request = self.factory.delete(USER_URL, format="json")
        response = self.view(request, username=username)
        return response

    def test_successful_delete_user(self):
        user = User.objects.create(**generate_new_user_payload())
        username = user.username
        response = self._build_delete_response(username)
        response.render()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_unsuccessful_delete_user_from_invalid_id(self):
        response = self._build_delete_response("!!123")
        response.render()

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGetRetrieve(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_by_id_view = UserViewSet.as_view({"get": "retrieve"})

    def test_successful_get_user(self):
        user = User.objects.create(**generate_new_user_payload())
        username = user.username
        request = self.factory.get(USER_URL, format="json")
        response = self.get_by_id_view(request, username=username)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(user.first_name, model_data.get("first_name"))
        self.assertEqual(user.last_name, model_data.get("last_name"))
        self.assertEqual(user.username, model_data.get("username"))
        self.assertEqual(user.email, model_data.get("email"))
        self.assertNotIn("password", model_data)  # Should be a write only field.

    def test_unsuccessful_get_user_from_invalid_id(self):
        request = self.factory.get(USER_URL, format="json")
        response = self.get_by_id_view(request, username="!!123")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGetList(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_all_view = UserViewSet.as_view({"get": "list"})

    def test_successful_get_all_users(self):
        User.objects.create(**generate_new_user_payload())
        User.objects.create(**generate_new_user_payload())

        request = self.factory.get(USER_URL, format="json")
        response = self.get_all_view(request)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        for user in model_data:
            self.assertIn("gardens", user)
            self.assertIn("first_name", user)
            self.assertIn("last_name", user)
            self.assertIn("username", user)
            self.assertNotIn("password", user)  # Should be a write only field.
            self.assertIn("email", user)


class TestPatch(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserViewSet.as_view({"patch": "partial_update"})

    def _build_patch_response(self, update_payload):
        user = User.objects.create(**generate_new_user_payload())
        username = user.username
        request = self.factory.patch(
            USER_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, username=username)
        return response

    def test_successful_partial_update_user(self):
        response = self._build_patch_response({"first_name": "Fooupdated"})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("gardens", model_data)
        self.assertEqual("Fooupdated", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))
        self.assertIn("username", model_data)
        self.assertEqual("FooBar@Whizzbang.com", model_data.get("email"))
        self.assertNotIn("password", model_data)  # Should be a write only field.

    def test_unsuccessful_partial_update_user_from_invalid_payload(self):
        response = self._build_patch_response({"first_name": "Foo_updated", "last_name": "Bar"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"first_name": ["Your first name can only contain letters and must be 3 or more characters long."]}
        )

    def test_unsuccessful_partial_update_user_from_invalid_id(self):
        request = self.factory.patch(
            USER_URL, {"first_name": "Foo_updated", "last_name": "Bar"}, format="json")
        response = self.view(request, username="!!123")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserViewSet.as_view({"post": "create"})

    def _build_post_response(self, payload):
        request = self.factory.post(
            USER_URL,
            payload,
            format="json"
        )
        response = self.view(request)
        return response

    def test_successful_create_user(self):
        new_user = generate_new_user_payload()
        response = self._build_post_response(new_user)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertIn("gardens", model_data)
        self.assertEqual("Foo", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))
        self.assertEqual("FooBar@whizzbang.com", model_data.get("email"))
        self.assertEqual(new_user["username"], model_data.get("username"))
        self.assertEqual(1, len(mail.outbox))  # assert welcome email was sent.

    def test_unsuccessful_create_user_from_invalid_payload(self):
        response = self._build_post_response(
            {
                "first_name": "Foo",
                "last_name": "Bar",
                "email": "FooBar.com",
                "username": "Foo",
                "password": "Secret"
            }
        )
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"email": ["Enter a valid email address."]}
        )


class TestPut(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserViewSet.as_view({"put": "update"})

    def _build_put_response(self, update_payload):
        user = User.objects.create(**generate_new_user_payload())
        username = user.username
        request = self.factory.put(
            USER_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, username=username)
        return response

    def test_successful_update_user(self):
        response = self._build_put_response(
            {
                "first_name": "Fooupdated",
                "last_name": "Bar",
                "username": "FooUser",
                "password": "secret",
                "email": "FooBar@Whizzbang.com"}
        )
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("gardens", model_data)
        self.assertEqual("Fooupdated", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))
        self.assertEqual("FooUser", model_data.get("username"))
        self.assertEqual("FooBar@Whizzbang.com", model_data.get("email"))
        self.assertNotIn("password", model_data)

    def test_unsuccessful_update_user_from_invalid_payload(self):
        response = self._build_put_response(
            {
                "first_name": "Foo_updated",
                "last_name": "Bar",
                "email": "FooBar@Whizzbang.com",
                "username": create_unique_username(),
                "password": "secret"
            })
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"first_name": ["Your first name can only contain letters and must be 3 or more characters long."]}
        )

    def test_unsuccessful_update_user_from_invalid_id(self):
        request = self.factory.put(
            USER_URL,
            {"first_name": "Fooupdated", "last_name": "Bar"},
            format="json"
        )
        response = self.view(request, username="!!123")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
