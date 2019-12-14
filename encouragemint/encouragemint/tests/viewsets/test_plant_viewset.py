import json
from uuid import UUID

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.models import Plant, Garden, Profile
from encouragemint.encouragemint.views import PlantViewSet

PLANT_URL = "/plant/"
TEST_PROFILE = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})
TEST_GARDEN = Garden.objects.create(**{"garden_name": "Foo", "profile": TEST_PROFILE})
SAMPLE_PLANT = {
    "scientific_name": "Eriophyllum lanatum",
    "common_name": "common woolly sunflower",
    "duration": "Annual, Perennial",
    "bloom_period": "Spring",
    "growth_period": "Summer",
    "growth_rate": "Slow",
    "shade_tolerance": "High",
    "moisture_use": "High",
    "family_common_name": "Aster family",
    "trefle_id": 134845
}
SAMPLE_NEW_PLANT_REQUEST = {
    "plant_name": "common woolly sunflower"
}


class TestDelete(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"delete": "destroy"})

    def _build_delete_response(self, plant_id):
        request = self.factory.delete(PLANT_URL, format="json")
        response = self.view(request, plant_id=plant_id)
        return response

    def test_delete_plant(self):
        plant = Plant.objects.create(**SAMPLE_PLANT, garden=TEST_GARDEN)
        plant_id = plant.plant_id
        response = self._build_delete_response(plant_id)
        response.render()
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_plant_by_invalid_id(self):
        plant_id = "Foo"
        response = self._build_delete_response(plant_id)
        response.render()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGetRetrieve(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_by_id_view = PlantViewSet.as_view({"get": "retrieve"})

    def test_get_plant(self):
        plant = Plant.objects.create(**SAMPLE_PLANT, garden=TEST_GARDEN)
        plant_id = plant.plant_id
        request = self.factory.get(PLANT_URL, format="json")
        response = self.get_by_id_view(request, plant_id=plant_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("plant_id", model_data)
        self.assertEqual(SAMPLE_PLANT.get("scientific_name"), model_data.get("scientific_name"))
        self.assertEqual(SAMPLE_PLANT.get("common_name"), model_data.get("common_name"))
        self.assertEqual(SAMPLE_PLANT.get("duration"), model_data.get("duration"))
        self.assertEqual(SAMPLE_PLANT.get("bloom_period"), model_data.get("bloom_period"))
        self.assertEqual(SAMPLE_PLANT.get("growth_period"), model_data.get("growth_period"))
        self.assertEqual(SAMPLE_PLANT.get("growth_rate"), model_data.get("growth_rate"))
        self.assertEqual(SAMPLE_PLANT.get("shade_tolerance"), model_data.get("shade_tolerance"))
        self.assertEqual(SAMPLE_PLANT.get("moisture_use"), model_data.get("moisture_use"))
        self.assertEqual(SAMPLE_PLANT.get("family_common_name"), model_data.get("family_common_name"))
        self.assertEqual(SAMPLE_PLANT.get("garden_id"), model_data.get("garden_id"))
        self.assertEqual(SAMPLE_PLANT.get("trefle_id"), model_data.get("trefle_id"))

    def test_get_plant_by_invalid_id(self):
        plant_id = "Foo"
        request = self.factory.get(PLANT_URL, format="json")
        response = self.get_by_id_view(request, plant_id=plant_id)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestGetList(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.get_all_view = PlantViewSet.as_view({"get": "list"})

    def test_get_all_plants(self):
        Plant.objects.create(**SAMPLE_PLANT, garden=TEST_GARDEN)
        Plant.objects.create(**SAMPLE_PLANT, garden=TEST_GARDEN)
        request = self.factory.get(PLANT_URL, format="json")
        response = self.get_all_view(request)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        for plant in model_data:
            self.assertIn("plant_id", plant)
            self.assertIn("scientific_name", plant)
            self.assertIn("common_name", plant)
            self.assertIn("duration", plant)
            self.assertIn("bloom_period", plant)
            self.assertIn("growth_period", plant)
            self.assertIn("growth_rate", plant)
            self.assertIn("shade_tolerance", plant)
            self.assertIn("moisture_use", plant)
            self.assertIn("family_common_name", plant)
            self.assertIn("garden", plant)
            self.assertIn("trefle_id", plant)


class TestPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"post": "create"})

    def _build_post_response(self, payload):
        request = self.factory.post(
            PLANT_URL,
            payload,
            format="json"
        )
        response = self.view(request)
        return response

    def test_create_plant(self):
        payload = SAMPLE_NEW_PLANT_REQUEST.copy()
        payload["garden"] = str(TEST_GARDEN.garden_id)
        response = self._build_post_response(payload)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))
        print(model_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertIn("plant_id", model_data)
        self.assertEqual(SAMPLE_PLANT.get("scientific_name"), model_data.get("scientific_name"))
        self.assertEqual(SAMPLE_PLANT.get("common_name"), model_data.get("common_name"))
        self.assertEqual(SAMPLE_PLANT.get("duration"), model_data.get("duration"))
        self.assertEqual(SAMPLE_PLANT.get("bloom_period"), model_data.get("bloom_period"))
        self.assertEqual(SAMPLE_PLANT.get("growth_period"), model_data.get("growth_period"))
        self.assertEqual(SAMPLE_PLANT.get("growth_rate"), model_data.get("growth_rate"))
        self.assertEqual(SAMPLE_PLANT.get("shade_tolerance"), model_data.get("shade_tolerance"))
        self.assertEqual(SAMPLE_PLANT.get("moisture_use"), model_data.get("moisture_use"))
        self.assertEqual(SAMPLE_PLANT.get("family_common_name"), model_data.get("family_common_name"))
        self.assertEqual(TEST_GARDEN.garden_id, UUID(model_data.get("garden")))
        self.assertEqual(SAMPLE_PLANT.get("trefle_id"), model_data.get("trefle_id"))


class TestPut(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"put": "update"})

    def _build_put_response(self, update_payload):
        existing_plant = SAMPLE_PLANT
        existing_plant["garden"] = TEST_GARDEN
        plant = Plant.objects.create(**existing_plant)
        plant_id = plant.plant_id
        request = self.factory.put(
            PLANT_URL,
            update_payload,
            format="json"
        )
        response = self.view(request, plant_id=plant_id)
        return response

    def test_update_plant(self):
        new_plant_details = SAMPLE_PLANT.copy()
        new_plant_details["scientific_name"] = "Fooupdated"
        new_plant_details["garden"] = str(TEST_GARDEN.garden_id)
        response = self._build_put_response(new_plant_details)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("plant_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("scientific_name"))
        self.assertEqual(SAMPLE_PLANT.get("common_name"), model_data.get("common_name"))
        self.assertEqual(SAMPLE_PLANT.get("duration"), model_data.get("duration"))
        self.assertEqual(SAMPLE_PLANT.get("bloom_period"), model_data.get("bloom_period"))
        self.assertEqual(SAMPLE_PLANT.get("growth_period"), model_data.get("growth_period"))
        self.assertEqual(SAMPLE_PLANT.get("growth_rate"), model_data.get("growth_rate"))
        self.assertEqual(SAMPLE_PLANT.get("shade_tolerance"), model_data.get("shade_tolerance"))
        self.assertEqual(SAMPLE_PLANT.get("moisture_use"), model_data.get("moisture_use"))
        self.assertEqual(SAMPLE_PLANT.get("family_common_name"), model_data.get("family_common_name"))
        self.assertEqual(TEST_GARDEN.garden_id, UUID(model_data.get("garden")))
        self.assertEqual(SAMPLE_PLANT.get("trefle_id"), model_data.get("trefle_id"))

    def test_update_plant_by_invalid_id(self):
        new_plant_details = SAMPLE_PLANT.copy()
        new_plant_details["scientific_name"] = "Fooupdated"
        new_plant_details["garden"] = str(TEST_GARDEN.garden_id)

        request = self.factory.put(
            PLANT_URL,
            new_plant_details,
            format="json"
        )
        response = self.view(request, plant_id="Foo")
        response.render()

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
