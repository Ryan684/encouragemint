import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.models import Profile
from encouragemint.encouragemint.serializers import ProfileSerializer
from encouragemint.encouragemint.views import ProfileViewSet

PROFILE_URL = "/profile/"
SAMPLE_PROFILE = {
    "first_name": "Foo",
    "last_name": "Bar"
}


class TestProfileViewsetParameters(TestCase):
    def test_viewset_parameters(self):
        self.assertEqual(
            ["get", "post", "put", "patch", "delete"], ProfileViewSet.http_method_names)
        self.assertEqual("profile_id", ProfileViewSet.lookup_field)
        self.assertEqual(ProfileSerializer, ProfileViewSet.serializer_class)


class TestDelete(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileViewSet.as_view({"delete": "destroy"})

    def _build_delete_response(self, profile_id):
        request = self.factory.delete(PROFILE_URL, format="json")
        response = self.view(request, profile_id=profile_id)
        return response

    def test_successful_delete_profile(self):
        profile = Profile.objects.create(**SAMPLE_PROFILE)
        profile_id = profile.profile_id
        response = self._build_delete_response(profile_id)
        response.render()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_unsuccessful_delete_profile_from_invalid_id(self):
        response = self._build_delete_response("Foo")
        response.render()

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGetRetrieve(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_by_id_view = ProfileViewSet.as_view({"get": "retrieve"})

    def test_successful_get_profile(self):
        profile = Profile.objects.create(**SAMPLE_PROFILE)
        profile_id = profile.profile_id
        request = self.factory.get(PROFILE_URL, format="json")
        response = self.get_by_id_view(request, profile_id=profile_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("profile_id", model_data)
        self.assertEqual(profile.first_name, model_data.get("first_name"))
        self.assertEqual(profile.last_name, model_data.get("last_name"))

    def test_unsuccessful_get_profile_from_invalid_id(self):
        request = self.factory.get(PROFILE_URL, format="json")
        response = self.get_by_id_view(request, profile_id="Foo")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGetList(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_all_view = ProfileViewSet.as_view({"get": "list"})

    def test_successful_get_all_profiles(self):
        Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})
        Profile.objects.create(**{"first_name": "Whizz", "last_name": "Bang"})
        request = self.factory.get(PROFILE_URL, format="json")
        response = self.get_all_view(request)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        for plant in model_data:
            self.assertIn("gardens", plant)
            self.assertIn("first_name", plant)
            self.assertIn("last_name", plant)


class TestPatch(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileViewSet.as_view({"patch": "partial_update"})

    def _build_patch_response(self, update_payload):
        profile = Profile.objects.create(**SAMPLE_PROFILE)
        profile_id = profile.profile_id
        request = self.factory.patch(
            PROFILE_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, profile_id=profile_id)
        return response

    def test_successful_partial_update_profile(self):
        response = self._build_patch_response({"first_name": "Fooupdated"})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("gardens", model_data)
        self.assertIn("profile_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))

    def test_unsuccessful_partial_update_profile_from_invalid_payload(self):
        response = self._build_patch_response({"first_name": "Foo_updated", "last_name": "Bar"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"first_name": ["Your first name can only contain letters."]}
        )

    def test_unsuccessful_partial_update_profile_from_invalid_id(self):
        request = self.factory.patch(
            PROFILE_URL, {"first_name": "Foo_updated", "last_name": "Bar"}, format="json")
        response = self.view(request, profile_id="Foo")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileViewSet.as_view({"post": "create"})

    def _build_post_response(self, payload):
        request = self.factory.post(
            PROFILE_URL,
            payload,
            format="json"
        )
        response = self.view(request)
        return response

    def test_successful_create_profile(self):
        response = self._build_post_response(SAMPLE_PROFILE)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertIn("gardens", model_data)
        self.assertIn("profile_id", model_data)
        self.assertEqual("Foo", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))

    def test_unsuccessful_create_profile_from_invalid_payload(self):
        response = self._build_post_response({"first_name": "F00", "last_name": "Bar"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"first_name": ["Your first name can only contain letters."]}
        )


class TestPut(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileViewSet.as_view({"put": "update"})

    def _build_put_response(self, update_payload):
        profile = Profile.objects.create(**SAMPLE_PROFILE)
        profile_id = profile.profile_id
        request = self.factory.put(
            PROFILE_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, profile_id=profile_id)
        return response

    def test_successful_update_profile(self):
        response = self._build_put_response({"first_name": "Fooupdated", "last_name": "Bar"})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("gardens", model_data)
        self.assertIn("profile_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))

    def test_unsuccessful_update_profile_from_invalid_payload(self):
        response = self._build_put_response({"first_name": "Foo_updated", "last_name": "Bar"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"first_name": ["Your first name can only contain letters."]}
        )

    def test_unsuccessful_update_profile_from_invalid_id(self):
        request = self.factory.put(
            PROFILE_URL,
            {"first_name": "Fooupdated", "last_name": "Bar"},
            format="json"
        )
        response = self.view(request, profile_id="Foo")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
