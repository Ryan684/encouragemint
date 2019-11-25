import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.models import Plant, Profile
from encouragemint.encouragemint.views import PlantViewSet

PLANT_URL = "/plant/"
TEST_PROFILE = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})
SAMPLE_PLANT_REQUEST = {"plant_name": "Foo"}


class TestDelete(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"delete": "destroy"})

    def build_delete_response(self, plant_id):
        request = self.factory.delete(PLANT_URL, format="json")
        response = self.view(request, plant_id=plant_id)
        return response

    def test_delete_plant(self):
        plant = Plant.objects.create(**SAMPLE_PLANT_REQUEST, profile=TEST_PROFILE)
        plant_id = plant.plant_id
        response = self.build_delete_response(plant_id)
        response.render()
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_plant_bad_id(self):
        plant_id = "Foo"
        response = self.build_delete_response(plant_id)
        response.render()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGet(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_by_id_view = PlantViewSet.as_view({"get": "retrieve"})
        self.get_all_view = PlantViewSet.as_view({"get": "list"})

    def test_get_all_plants(self):
        Plant.objects.create(**{"plant_name": "Fooflower"}, profile=TEST_PROFILE)
        Plant.objects.create(**{"plant_name": "Barflower"}, profile=TEST_PROFILE)
        request = self.factory.get(PLANT_URL, format="json")
        response = self.get_all_view(request)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("plant_id", model_data[0])
        self.assertEqual("Barflower", model_data[0].get("plant_name"))
        self.assertIn("plant_id", model_data[1])
        self.assertEqual("Fooflower", model_data[1].get("plant_name"))

    def test_get_plant_by_valid_id(self):
        plant = Plant.objects.create(**SAMPLE_PLANT_REQUEST, profile=TEST_PROFILE)
        plant_id = plant.plant_id
        request = self.factory.get(PLANT_URL, format="json")
        response = self.get_by_id_view(request, plant_id=plant_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("plant_id", model_data)
        self.assertEqual(plant.plant_name, model_data.get("plant_name"))

    def test_get_plant_by_invalid_id(self):
        plant_id = "Foo"
        request = self.factory.get(PLANT_URL, format="json")
        response = self.get_by_id_view(request, plant_id=plant_id)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestPatch(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"patch": "partial_update"})

    def build_patch_response(self, update_payload):
        plant = Plant.objects.create(**SAMPLE_PLANT_REQUEST, profile=TEST_PROFILE)
        plant_id = plant.plant_id
        request = self.factory.patch(
            PLANT_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, plant_id=plant_id)
        return response

    def test_partial_update_plant(self):
        response = self.build_patch_response({"plant_name": "Fooupdated"})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("plant_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("plant_name"))

    def test_partial_update_plant_with_profile(self):
        response = self.build_patch_response({"plant_name": "Fooupdated", "profile": str(TEST_PROFILE.profile_id)})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("plant_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("plant_name"))

    def test_invalid_plant_name_no_profile(self):
        response = self.build_patch_response({"plant_name": "Foo_updated"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"plant_name": ["A plant's name can only contain letters."]}
        )

    def test_invalid_plant_name(self):
        response = self.build_patch_response({"plant_name": "Foo_updated", "profile": str(TEST_PROFILE.profile_id)})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"plant_name": ["A plant's name can only contain letters."]}
        )


class TestPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"post": "create"})

    def build_post_response(self, payload):
        request = self.factory.post(
            PLANT_URL,
            payload,
            format="json"
        )
        response = self.view(request)
        return response

    def test_create_plant(self):
        payload = SAMPLE_PLANT_REQUEST
        payload["profile_id"] = str(TEST_PROFILE.profile_id)
        response = self.build_post_response(payload)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertIn("plant_id", model_data)
        self.assertIn("profile", model_data)
        self.assertEqual("Foo", model_data.get("plant_name"))

    def test_invalid_plant_name_no_profile(self):
        response = self.build_post_response({"plant_name": "F00"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"plant_name": ["A plant's name can only contain letters."], "profile_id": ["This field is required."]}
        )

    def test_invalid_plant_name(self):
        response = self.build_post_response({"plant_name": "F00", "profile_id": str(TEST_PROFILE.profile_id)})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"plant_name": ["A plant's name can only contain letters."]}
        )


class TestPut(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"put": "update"})

    def build_put_response(self, update_payload):
        plant = Plant.objects.create(**SAMPLE_PLANT_REQUEST, profile=TEST_PROFILE)
        plant_id = plant.plant_id
        request = self.factory.put(
            PLANT_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, plant_id=plant_id)
        return response

    def test_update_plant(self):
        response = self.build_put_response({"plant_name": "Fooupdated", "profile_id": str(TEST_PROFILE.profile_id)})
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIn("plant_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("plant_name"))

    def test_invalid_plant_name_no_profile(self):
        response = self.build_put_response({"plant_name": "Foo_updated"})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"plant_name": ["A plant's name can only contain letters."], "profile_id": ["This field is required."]}

        )

    def test_invalid_plant_name(self):
        response = self.build_put_response({"plant_name": "Foo_updated", "profile_id": str(TEST_PROFILE.profile_id)})
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"plant_name": ["A plant's name can only contain letters."]}
        )
