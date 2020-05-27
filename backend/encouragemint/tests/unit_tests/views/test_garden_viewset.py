import json
from unittest.mock import patch

from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIRequestFactory

from backend.encouragemint.models.garden import Garden
from backend.encouragemint.models.profile import Profile
from backend.encouragemint.serializers.garden_serializer import GardenSerializer
from backend.encouragemint.tests.helpers import create_test_garden, SAMPLE_GARDEN
from backend.encouragemint.views.garden_viewset import GardenViewSet

GARDEN_URL = "/garden/"
TEST_PROFILE = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})


class TestGardenViewsetParameters(TestCase):
    def test_viewset_parameters(self):
        self.assertEqual(["get", "post", "patch", "delete"], GardenViewSet.http_method_names)
        self.assertEqual("garden_id", GardenViewSet.lookup_field)
        self.assertEqual(GardenSerializer, GardenViewSet.serializer_class)


class TestDelete(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GardenViewSet.as_view({"delete": "destroy"})

    def _build_delete_response(self, garden_id):
        request = self.factory.delete(GARDEN_URL, format="json")
        response = self.view(request, garden_id=garden_id)
        return response

    def test_successful_delete_garden(self):
        garden = create_test_garden()
        garden_id = garden.get("garden_id")
        response = self._build_delete_response(garden_id)
        response.render()

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_unsuccessful_delete_garden_from_invalid_id(self):
        response = self._build_delete_response("Foo")
        response.render()

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGetRetrieve(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_by_id_view = GardenViewSet.as_view({"get": "retrieve"})

    def test_successful_get_garden(self):
        garden = Garden.objects.create(profile=TEST_PROFILE, **SAMPLE_GARDEN)
        garden_id = garden.garden_id
        request = self.factory.get(GARDEN_URL, format="json")
        response = self.get_by_id_view(request, garden_id=garden_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("garden_id", model_data)
        self.assertEqual(garden.location, model_data.get("location"))
        self.assertEqual(str(garden.profile.profile_id), model_data.get("profile"))
        self.assertEqual(garden.direction, model_data.get("direction"))
        self.assertEqual(garden.garden_name, model_data.get("garden_name"))
        self.assertIsNone(garden.latitude)
        self.assertIsNone(garden.longitude)

    def test_unsuccessful_get_garden_from_invalid_id(self):
        request = self.factory.get(GARDEN_URL, format="json")
        response = self.get_by_id_view(request, garden_id="Foo")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGetList(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_all_view = GardenViewSet.as_view({"get": "list"})

    def test_successful_get_all_gardens(self):
        Garden.objects.create(profile=TEST_PROFILE, **SAMPLE_GARDEN)
        Garden.objects.create(profile=TEST_PROFILE, **SAMPLE_GARDEN)
        request = self.factory.get(GARDEN_URL, format="json")
        response = self.get_all_view(request)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        for garden in model_data:
            self.assertIn("garden_id", garden)
            self.assertIn("location", garden)
            self.assertIn("profile", garden)
            self.assertIn("direction", garden)
            self.assertIn("garden_id", garden)
            self.assertIn("latitude", garden)
            self.assertIn("longitude", garden)


class TestPatch(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GardenViewSet.as_view({"patch": "partial_update"})

    def _build_patch_response(self, update_payload):
        garden = create_test_garden()
        garden_id = garden.get("garden_id")
        request = self.factory.patch(
            GARDEN_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, garden_id=garden_id)
        return response

    @patch("backend.encouragemint.views.garden_viewset.add_garden_location")
    def test_successful_partial_update_garden(self, mock_add_garden_location):
        response = self._build_patch_response({"garden_name": "Fooupdated", "direction": "north"})

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        mock_add_garden_location.delay.assert_called_once()

    def test_unsuccessful_partial_update_garden_from_invalid_payload(self):
        response = self._build_patch_response({"garden_name": "Foo_updated", "direction": "north"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {
                "garden_name": [
                    "Invalid entry for the garden's name. A garden's name can "
                    "only contain letters, numbers, hyphens, spaces and apostrophes."
                ]
            }
        )

    def test_unsuccessful_partial_update_garden_from_invalid_id(self):
        request = self.factory.patch(
            GARDEN_URL, {"garden_name": "Foo_updated", "direction": "north"}, format="json")
        response = self.view(request, garden_id="Foo")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


@override_settings(GOOGLE_API_KEY="Foo")
class TestPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GardenViewSet.as_view({"post": "create"})

    def _build_post_response(self, payload):
        request = self.factory.post(
            GARDEN_URL,
            payload,
            format="json"
        )
        response = self.view(request)
        return response

    @patch("backend.encouragemint.views.garden_viewset.add_garden_location")
    def test_successful_create_garden(self, mock_add_garden_location):
        payload = SAMPLE_GARDEN
        payload["profile"] = str(TEST_PROFILE.profile_id)
        response = self._build_post_response(payload)

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        mock_add_garden_location.delay.assert_called_once()

    def test_unsuccessful_create_garden_from_invalid_payload(self):
        response = self._build_post_response({
            "garden_name": "F00$",
            "direction": SAMPLE_GARDEN.get("direction"),
            "profile": str(TEST_PROFILE.profile_id),
            "location": SAMPLE_GARDEN.get("location")
        })
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {
                "garden_name": [
                    "Invalid entry for the garden's name. A garden's name can "
                    "only contain letters, numbers, hyphens, spaces and apostrophes."
                ]
            }
        )
