import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.views import ProfileViewSet
from encouragemint.encouragemint.models import Profile

PROFILE_URL = "/profile/"
SAMPLE_PROFILE = {
    "first_name": "Foo",
    "last_name": "Bar"
}


class TestDelete(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileViewSet.as_view({"delete": "destroy"})

    def build_delete_response(self, profile_id):
        request = self.factory.delete(PROFILE_URL, format="json")
        response = self.view(request, profile_id=profile_id)
        return response

    def test_delete_profile(self):
        profile = Profile.objects.create(**SAMPLE_PROFILE)
        profile_id = profile.profile_id
        response = self.build_delete_response(profile_id)
        response.render()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_profile_bad_id(self):
        profile_id = "Foo"
        response = self.build_delete_response(profile_id)
        response.render()

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_by_id_view = ProfileViewSet.as_view({"get": "retrieve"})
    #
    #     self.get_all_view = ProfileViewSet.as_view({"get": "list"})
    #
    # def test_get_all_profiles(self):
    #     Profile.objects.create(**{"first_name": "Jane", "last_name": "Doe"})
    #     Profile.objects.create(**{"first_name": "Joe", "last_name": "Blogs"})
    #     request = self.factory.get(PROFILE_URL, format="json")
    #     response = self.get_all_view(request)
    #     response.render()
    #     model_data = json.loads(response.content.decode("utf-8"))
    #
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertIn("profile_id", model_data[0])
    #     self.assertEqual("Jane", model_data[0].get("first_name"))
    #     self.assertEqual("Doe", model_data[0].get("last_name"))
    #     self.assertIn("profile_id", model_data[1])
    #     self.assertEqual("Joe", model_data[1].get("first_name"))
    #     self.assertEqual("Blogs", model_data[1].get("last_name"))

    def test_get_a_profile_by_valid_id(self):
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

    def test_get_profile_by_invalid_id(self):
        profile_id = "Foo"
        request = self.factory.get(PROFILE_URL, format="json")
        response = self.get_by_id_view(request, profile_id=profile_id)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestPatch(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileViewSet.as_view({"patch": "partial_update"})

    def build_patch_response(self, update_payload):
        profile = Profile.objects.create(**SAMPLE_PROFILE)
        profile_id = profile.profile_id
        request = self.factory.patch(
            PROFILE_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, profile_id=profile_id)
        return response

    def test_partial_update_profile(self):
        response = self.build_patch_response({"first_name": "Fooupdated"})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("gardens", model_data)
        self.assertIn("profile_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))

    def test_invalid_first_name(self):
        response = self.build_patch_response({"first_name": "Foo_updated", "last_name": "Bar"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"first_name": ["Your first name can only contain letters."]}
        )

    def test_invalid_last_name(self):
        response = self.build_patch_response({"first_name": "Foo", "last_name": "B@R"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"last_name": ["Your last name can only contain letters."]}
        )


class TestPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileViewSet.as_view({"post": "create"})

    def build_post_response(self, payload):
        request = self.factory.post(
            PROFILE_URL,
            payload,
            format="json"
        )
        response = self.view(request)
        return response

    def test_create_profile(self):
        response = self.build_post_response(SAMPLE_PROFILE)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertIn("gardens", model_data)
        self.assertIn("profile_id", model_data)
        self.assertEqual("Foo", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))

    def test_invalid_first_name(self):
        response = self.build_post_response({"first_name": "F00", "last_name": "Bar"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"first_name": ["Your first name can only contain letters."]}
        )

    def test_invalid_last_name(self):
        response = self.build_post_response({"first_name": "Foo", "last_name": "B4r"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"last_name": ["Your last name can only contain letters."]}
        )


class TestPut(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProfileViewSet.as_view({"put": "update"})

    def build_put_response(self, update_payload):
        profile = Profile.objects.create(**SAMPLE_PROFILE)
        profile_id = profile.profile_id
        request = self.factory.put(
            PROFILE_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, profile_id=profile_id)
        return response

    def test_update_profile(self):
        response = self.build_put_response({"first_name": "Fooupdated", "last_name": "Bar"})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("gardens", model_data)
        self.assertIn("profile_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("first_name"))
        self.assertEqual("Bar", model_data.get("last_name"))

    def test_invalid_first_name(self):
        response = self.build_put_response({"first_name": "Foo_updated", "last_name": "Bar"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"first_name": ["Your first name can only contain letters."]}
        )

    def test_invalid_last_name(self):
        response = self.build_put_response({"first_name": "Foo", "last_name": "Bar_updated"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"last_name": ["Your last name can only contain letters."]}
        )
