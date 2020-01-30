import json
from unittest.mock import patch
from uuid import UUID, uuid4

from django.core import exceptions
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint import models
from encouragemint.encouragemint.models import Plant, Garden, Profile
from encouragemint.encouragemint.tests.unit_tests.viewsets.helpers import SAMPLE_PLANT
from encouragemint.encouragemint.views import PlantViewSet
from encouragemint.lib.trefle.exceptions import TrefleConnectionError

PLANT_URL = "/plant/"
TEST_PROFILE = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})
TEST_GARDEN = Garden.objects.create(
    **{
        "garden_name": "Foo",
        "profile": TEST_PROFILE,
        "direction": "north",
        "location": "Truro, UK",
        "latitude": 50.263195,
        "longitude": -5.051041
    }
)
PLANT_DATA = SAMPLE_PLANT.copy()


class TestPlantViewsetParameters(TestCase):
    def test_viewset_parameters(self):
        plant_viewset = PlantViewSet
        self.assertEqual(["post", "put", "delete"], plant_viewset.http_method_names)
        self.assertEqual("plant_id", plant_viewset.lookup_field)
        self.assertEqual(None, plant_viewset.serializer_class)


class TestDelete(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"delete": "destroy"})

    def _build_delete_response(self, plant_id):
        request = self.factory.delete(PLANT_URL, format="json")
        response = self.view(request, plant_id=plant_id)
        return response

    def test_successful_delete_plant(self):
        plant = Plant.objects.create(**PLANT_DATA, garden=TEST_GARDEN)
        plant_id = plant.plant_id
        response = self._build_delete_response(plant_id)
        response.render()
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_unsuccessful_delete_plant_from_invalid_id(self):
        response = self._build_delete_response("Foo")
        response.render()
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class TestPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"post": "create"})
        self.new_plant_request = {
            "plant_name": "common woolly sunflower",
            "garden": str(TEST_GARDEN.garden_id)
        }

        patcher = patch("encouragemint.encouragemint.views.TREFLE.lookup_plants")
        self.mock_trefle = patcher.start()
        self.addCleanup(patcher.stop)

    def _build_post_response(self, payload):
        request = self.factory.post(
            PLANT_URL,
            payload,
            format="json"
        )
        response = self.view(request)
        return response

    def test_successful_create_plant(self):
        self.mock_trefle.return_value = PLANT_DATA

        payload = self.new_plant_request.copy()
        response = self._build_post_response(payload)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertIn("plant_id", model_data)
        self.assertEqual(PLANT_DATA.get("scientific_name"), model_data.get("scientific_name"))
        self.assertEqual(PLANT_DATA.get("common_name"), model_data.get("common_name"))
        self.assertEqual(PLANT_DATA.get("duration"), model_data.get("duration"))
        self.assertEqual(PLANT_DATA.get("bloom_period"), model_data.get("bloom_period"))
        self.assertEqual(PLANT_DATA.get("growth_period"), model_data.get("growth_period"))
        self.assertEqual(PLANT_DATA.get("growth_rate"), model_data.get("growth_rate"))
        self.assertEqual(PLANT_DATA.get("shade_tolerance"), model_data.get("shade_tolerance"))
        self.assertEqual(PLANT_DATA.get("moisture_use"), model_data.get("moisture_use"))
        self.assertEqual(
            PLANT_DATA.get("family_common_name"), model_data.get("family_common_name"))
        self.assertEqual(TEST_GARDEN.garden_id, UUID(model_data.get("garden")))
        self.assertEqual(PLANT_DATA.get("trefle_id"), model_data.get("trefle_id"))

    def test_unsuccessful_create_plant_from_invalid_payload(self):
        payload = self.new_plant_request.copy()
        payload["plant_name"] = "F00"
        response = self._build_post_response(payload)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertDictEqual(
            json.loads(response.content.decode("utf-8")),
            {"plant_name": ["Invalid entry for the plant's's name. A garden's name can only "
                            "contain letters, hyphens, spaces and apostrophes."]}
        )

    def test_unsuccessful_create_plant_from_trefle_exception(self):
        self.mock_trefle.side_effect = TrefleConnectionError
        payload = self.new_plant_request.copy()
        response = self._build_post_response(payload)
        response.render()

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        self.assertEqual(
            {"Message": "Encouragemint can't add new plants right now. Try again later."},
            response.data
        )

    def test_successful_create_plant_many_trefle_results(self):
        test_responses_dir = "encouragemint/lib/trefle/tests/test_responses"
        with open(f"{test_responses_dir}/plant_search_many_matches.json", "r") as file:
            search_many_matches = json.load(file)

        self.mock_trefle.return_value = search_many_matches
        payload = self.new_plant_request.copy()
        response = self._build_post_response(payload)
        response.render()

        self.assertEqual(status.HTTP_300_MULTIPLE_CHOICES, response.status_code)
        self.assertEqual(
            search_many_matches,
            response.data
        )

    def test_unsuccessful_create_plant_from_no_trefle_results(self):
        self.mock_trefle.return_value = []
        payload = self.new_plant_request.copy()
        response = self._build_post_response(payload)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {"Message": "Encouragemint couldn't find any plants with that name."},
            response.data
        )


class TestPut(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PlantViewSet.as_view({"put": "update"})

        patcher = patch("encouragemint.encouragemint.views.TREFLE.lookup_plants")
        self.mock_trefle = patcher.start()
        self.addCleanup(patcher.stop)

    def _build_put_response(self):
        existing_plant = PLANT_DATA.copy()
        existing_plant["garden"] = TEST_GARDEN
        plant = Plant.objects.create(**existing_plant)
        plant_id = plant.plant_id
        request = self.factory.put(
            PLANT_URL,
            format="json"
        )
        return self.view(request, plant_id=plant_id)

    def test_successful_update_plant(self):
        updated_plant = PLANT_DATA.copy()
        updated_plant["scientific_name"] = "Fooupdated"
        self.mock_trefle.return_value = updated_plant

        response = self._build_put_response()
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.assertIn("plant_id", model_data)
        self.assertEqual("Fooupdated", model_data.get("scientific_name"))
        self.assertEqual(PLANT_DATA.get("common_name"), model_data.get("common_name"))
        self.assertEqual(PLANT_DATA.get("duration"), model_data.get("duration"))
        self.assertEqual(PLANT_DATA.get("bloom_period"), model_data.get("bloom_period"))
        self.assertEqual(PLANT_DATA.get("growth_period"), model_data.get("growth_period"))
        self.assertEqual(PLANT_DATA.get("growth_rate"), model_data.get("growth_rate"))
        self.assertEqual(PLANT_DATA.get("shade_tolerance"), model_data.get("shade_tolerance"))
        self.assertEqual(PLANT_DATA.get("moisture_use"), model_data.get("moisture_use"))
        self.assertEqual(
            PLANT_DATA.get("family_common_name"), model_data.get("family_common_name"))
        self.assertEqual(TEST_GARDEN.garden_id, UUID(model_data.get("garden")))
        self.assertEqual(PLANT_DATA.get("trefle_id"), model_data.get("trefle_id"))

    def test_unsuccessful_update_plant_from_trefle_exception(self):
        self.mock_trefle.side_effect = TrefleConnectionError
        response = self._build_put_response()
        response.render()

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        self.assertEqual(
            {"Message": "Encouragemint can't update plants right now. Try again later."},
            response.data
        )

    def test_unsuccessful_update_plant_from_invalid_id(self):
        new_plant_details = PLANT_DATA.copy()
        new_plant_details["scientific_name"] = "Fooupdated"
        new_plant_details["garden"] = str(TEST_GARDEN.garden_id)

        request = self.factory.put(
            PLANT_URL,
            new_plant_details,
            format="json"
        )

        self.assertRaises(exceptions.ValidationError, self.view, request, plant_id="Foo")
        self.assertRaises(models.Plant.DoesNotExist, self.view, request, plant_id=uuid4())
