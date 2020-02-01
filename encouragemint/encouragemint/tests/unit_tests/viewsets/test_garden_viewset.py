import json
from unittest.mock import patch, Mock

from django.test import TestCase, override_settings
from geopy.exc import GeocoderServiceError
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.models import Profile
from encouragemint.encouragemint.serializers import GardenSerializer
from encouragemint.encouragemint.tests.helpers import create_test_garden, SAMPLE_GARDEN, \
    SAMPLE_GARDEN_SUNLIGHT, SAMPLE_GARDEN_GEOCODE_LOCATION
from encouragemint.encouragemint.views import GardenViewSet

GARDEN_URL = "/garden/"
TEST_PROFILE = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})


class TestGardenViewsetParameters(TestCase):
    def test_viewset_parameters(self):
        self.assertEqual(["post", "put", "patch", "delete"], GardenViewSet.http_method_names)
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

    def test_successful_partial_update_garden(self):
        response = self._build_patch_response({"garden_name": "Fooupdated", "direction": "north"})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("plants", model_data)
        self.assertIn("garden_id", model_data)
        self.assertIn("profile", model_data)
        self.assertEqual("Fooupdated", model_data.get("garden_name"))
        self.assertEqual(SAMPLE_GARDEN.get("direction"), model_data.get("direction"))
        self.assertEqual(SAMPLE_GARDEN_SUNLIGHT, model_data.get("sunlight"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("address"),
                         model_data.get("location"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("longitude"),
                         model_data.get("longitude"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("latitude"),
                         model_data.get("latitude"))

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

        patcher = patch("geopy.geocoders.googlev3.GoogleV3.geocode")
        self.mock_google = patcher.start()
        self.addCleanup(patcher.stop)

    def _build_post_response(self, payload):
        request = self.factory.post(
            GARDEN_URL,
            payload,
            format="json"
        )
        response = self.view(request)
        return response

    def test_successful_create_garden(self):
        mock = Mock(**SAMPLE_GARDEN_GEOCODE_LOCATION)
        self.mock_google.return_value = mock

        payload = SAMPLE_GARDEN
        payload["profile"] = str(TEST_PROFILE.profile_id)
        response = self._build_post_response(payload)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertIn("plants", model_data)
        self.assertIn("garden_id", model_data)
        self.assertIn("profile", model_data)
        self.assertEqual(SAMPLE_GARDEN.get("garden_name"), model_data.get("garden_name"))
        self.assertEqual(SAMPLE_GARDEN.get("direction"), model_data.get("direction"))
        self.assertEqual(SAMPLE_GARDEN_SUNLIGHT, model_data.get("sunlight"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("address"),
                         model_data.get("location"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("longitude"),
                         model_data.get("longitude"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("latitude"),
                         model_data.get("latitude"))

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

    def test_unsuccessful_create_garden_from_geocoder_exception(self):
        self.mock_google.side_effect = GeocoderServiceError

        request = self.factory.post(
            GARDEN_URL,
            SAMPLE_GARDEN,
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        self.assertEqual(
            {"Message": "Encouragemint can't create new gardens right now. Try again later."},
            response.data
        )

    def test_unsuccessful_create_garden_from_geocoder_location_not_found(self):
        self.mock_google.return_value = None

        request = self.factory.post(
            GARDEN_URL,
            SAMPLE_GARDEN,
            format="json"
        )
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {"Message": "Encouragemint couldn't find that location. Try to be more accurate."},
            response.data
        )


class TestPut(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = GardenViewSet.as_view({"put": "update"})

    def _build_put_response(self, update_payload):
        garden = create_test_garden()
        garden_id = garden.get("garden_id")
        request = self.factory.put(
            GARDEN_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, garden_id=garden_id)
        return response

    def test_successful_update_garden(self):
        new_garden_details = SAMPLE_GARDEN.copy()
        new_garden_details["garden_name"] = "Fooupdated"
        new_garden_details["profile"] = str(TEST_PROFILE.profile_id)
        response = self._build_put_response(new_garden_details)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("plants", model_data)
        self.assertIn("profile", model_data)
        self.assertIn("garden_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("garden_name"))
        self.assertEqual(SAMPLE_GARDEN.get("direction"), model_data.get("direction"))
        self.assertEqual(SAMPLE_GARDEN_SUNLIGHT, model_data.get("sunlight"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("address"),
                         model_data.get("location"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("longitude"),
                         model_data.get("longitude"))
        self.assertEqual(SAMPLE_GARDEN_GEOCODE_LOCATION.get("latitude"),
                         model_data.get("latitude"))

    def test_unsuccessful_update_garden_from_invalid_payload(self):
        response = self._build_put_response({
            "garden_name": "Foo_updated",
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

    def test_unsuccessful_update_garden_from_invalid_id(self):
        request = self.factory.put(
            GARDEN_URL,
            {
                "garden_name": "Fooupdated",
                "direction": SAMPLE_GARDEN.get("direction"),
                "profile": str(TEST_PROFILE.profile_id),
                "location": SAMPLE_GARDEN.get("location")
            },
            format="json"
        )
        response = self.view(request, garden_id="Foo")

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
