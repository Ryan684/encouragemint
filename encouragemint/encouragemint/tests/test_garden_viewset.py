import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.models import Garden, Profile
from encouragemint.encouragemint.views import GardenViewSet

GARDEN_URL = "/garden/"
TEST_PROFILE = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})
SAMPLE_GARDEN_REQUEST = {"garden_name": "Foo"}


class TestDelete(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GardenViewSet.as_view({"delete": "destroy"})

    def build_delete_response(self, garden_id):
        request = self.factory.delete(GARDEN_URL, format="json")
        response = self.view(request, garden_id=garden_id)
        return response

    def test_delete_garden(self):
        garden = Garden.objects.create(**SAMPLE_GARDEN_REQUEST, profile=TEST_PROFILE)
        garden_id = garden.garden_id
        response = self.build_delete_response(garden_id)
        response.render()
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_garden_bad_id(self):
        garden_id = "Foo"
        response = self.build_delete_response(garden_id)
        response.render()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_by_id_view = GardenViewSet.as_view({"get": "retrieve"})
    #
    #     Failing for some reason? Works if I run in isolation of other VieSset tests? Bad teardowns of tests?
    #
    #     self.get_all_view = GardenViewSet.as_view({"get": "list"})
    #
    # def test_get_all_gardens(self):
    #     Garden.objects.create(**{"garden_name": "Fooflower"}, profile=TEST_PROFILE)
    #     Garden.objects.create(**{"garden_name": "Barflower"}, profile=TEST_PROFILE)
    #     request = self.factory.get(GARDEN_URL, format="json")
    #     response = self.get_all_view(request)
    #     response.render()
    #     model_data = json.loads(response.content.decode("utf-8"))
    #
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertIn("garden_id", model_data[0])
    #     self.assertEqual("Fooflower", model_data[0].get("garden_name"))
    #     self.assertIn("garden_id", model_data[1])
    #     self.assertEqual("Barflower", model_data[1].get("garden_name"))

    def test_get_garden_by_valid_id(self):
        garden = Garden.objects.create(**SAMPLE_GARDEN_REQUEST, profile=TEST_PROFILE)
        garden_id = garden.garden_id
        request = self.factory.get(GARDEN_URL, format="json")
        response = self.get_by_id_view(request, garden_id=garden_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("garden_id", model_data)
        self.assertEqual(garden.garden_name, model_data.get("garden_name"))

    def test_get_garden_by_invalid_id(self):
        garden_id = "Foo"
        request = self.factory.get(GARDEN_URL, format="json")
        response = self.get_by_id_view(request, garden_id=garden_id)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestPatch(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GardenViewSet.as_view({"patch": "partial_update"})

    def build_patch_response(self, update_payload):
        garden = Garden.objects.create(**SAMPLE_GARDEN_REQUEST, profile=TEST_PROFILE)
        garden_id = garden.garden_id
        request = self.factory.patch(
            GARDEN_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, garden_id=garden_id)
        return response

    def test_partial_update_garden(self):
        response = self.build_patch_response({"garden_name": "Fooupdated"})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("garden_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("garden_name"))

    def test_partial_update_garden_with_profile(self):
        response = self.build_patch_response({"garden_name": "Fooupdated", "profile": str(TEST_PROFILE.profile_id)})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("garden_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("garden_name"))

    def test_invalid_garden_name_no_profile(self):
        response = self.build_patch_response({"garden_name": "Foo_updated"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"garden_name": ["A garden's name can only contain letters."]}
        )

    def test_invalid_garden_name(self):
        response = self.build_patch_response({"garden_name": "Foo_updated", "profile": str(TEST_PROFILE.profile_id)})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"garden_name": ["A garden's name can only contain letters."]}
        )


class TestPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GardenViewSet.as_view({"post": "create"})

    def build_post_response(self, payload):
        request = self.factory.post(
            GARDEN_URL,
            payload,
            format="json"
        )
        response = self.view(request)
        return response

    def test_create_garden(self):
        payload = SAMPLE_GARDEN_REQUEST
        payload["profile_id"] = str(TEST_PROFILE.profile_id)
        response = self.build_post_response(payload)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn("garden_id", model_data)
        self.assertIn("profile", model_data)
        self.assertEqual("Foo", model_data.get("garden_name"))

    def test_invalid_garden_name_no_profile(self):
        response = self.build_post_response({"garden_name": "F00"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"garden_name": ["A garden's name can only contain letters."], "profile_id": ["This field is required."]}
        )

    def test_invalid_garden_name(self):
        response = self.build_post_response({"garden_name": "F00", "profile_id": str(TEST_PROFILE.profile_id)})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"garden_name": ["A garden's name can only contain letters."]}
        )


class TestPut(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GardenViewSet.as_view({"put": "update"})

    def build_put_response(self, update_payload):
        garden = Garden.objects.create(**SAMPLE_GARDEN_REQUEST, profile=TEST_PROFILE)
        garden_id = garden.garden_id
        request = self.factory.put(
            GARDEN_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, garden_id=garden_id)
        return response

    def test_update_garden(self):
        response = self.build_put_response({"garden_name": "Fooupdated", "profile_id": str(TEST_PROFILE.profile_id)})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("garden_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("garden_name"))

    def test_invalid_garden_name_no_profile(self):
        response = self.build_put_response({"garden_name": "Foo_updated"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"garden_name": ["A garden's name can only contain letters."], "profile_id": ["This field is required."]}

        )

    def test_invalid_garden_name(self):
        response = self.build_put_response({"garden_name": "Foo_updated", "profile_id": str(TEST_PROFILE.profile_id)})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"garden_name": ["A garden's name can only contain letters."]}
        )
