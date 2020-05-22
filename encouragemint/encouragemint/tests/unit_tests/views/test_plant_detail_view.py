import json
from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.tests.helpers import TREFLE_ID_LOOKUP_RESPONSE
from encouragemint.encouragemint.views.plant_detail_view import plant_detail
from encouragemint.interfaces.trefle.exceptions import TrefleConnectionError


class TestPlantDetailView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = plant_detail
        self.trefle_id = "123456"
        self.plant_detail_url = "/plant-detail/"

        trefle_patcher = patch("encouragemint.encouragemint.views.plant_detail_view.lookup_plant_by_id")
        self.mock_trefle = trefle_patcher.start()
        self.addCleanup(trefle_patcher.stop)

    def test_unsuccessful_request_from_no_trefle_id_parameter(self):
        request = self.factory.get(self.plant_detail_url, format="json")
        response = self.view(request)
        response.render()

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                "message": "You must specify a trefle_id path parameter for plant details."
            },
            response.data
        )

    def test_valid_request_with_result(self):
        self.mock_trefle.return_value = TREFLE_ID_LOOKUP_RESPONSE
        expected_result = {
            "scientific_name": "Eriophyllum lanatum",
            "common_name": "common woolly sunflower",
            "images": [
                {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/b/b9/Eriophyllum_lanatum_3575.JPG"
                }
            ]
        }

        request = self.factory.get(f"{self.plant_detail_url}", format="json")
        response = self.view(request, trefle_id=self.trefle_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_result, model_data)

    def test_valid_request_with_no_result(self):
        self.mock_trefle.return_value = []

        request = self.factory.get(f"{self.plant_detail_url}", format="json")
        response = self.view(request, trefle_id=self.trefle_id)
        response.render()
        model_data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(
            {
                "message": "no plants could be found for this trefle_id."
            },
            model_data
        )

    def test_request_fails_if_trefle_down(self):
        self.mock_trefle.side_effect = TrefleConnectionError

        request = self.factory.get(f"{self.plant_detail_url}", format="json")
        response = self.view(request, trefle_id=self.trefle_id)
        response.render()

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
        self.assertEqual(
            {
                "message": "Encouragemint can't find details on this plant right now. "
                           "Try again later."
            },
            response.data
        )
