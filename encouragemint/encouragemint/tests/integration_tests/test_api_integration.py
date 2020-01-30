from unittest.mock import patch, Mock

from django.test import TestCase, override_settings

from rest_framework import status

from encouragemint.encouragemint.models import Profile, Plant, Garden
from encouragemint.encouragemint.tests.unit_tests.viewsets.helpers import create_test_garden, \
    SAMPLE_GARDEN_GEOCODE_LOCATION, SAMPLE_PLANT, TREFLE_NAME_LOOKUP_RESPONSE, TREFLE_ID_LOOKUP_RESPONSE


class TestProfile(TestCase):
    def setUp(self):
        self.url = "/profile/"
        self.data = {"first_name": "Foo", "last_name": "Bar"}
        self.test_profile = Profile.objects.create(**self.data)

    def test_create_profile(self):
        response = self.client.post(self.url, self.data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_retrieve_profile(self):
        response = self.client.get(self.url + f"{self.test_profile.profile_id}/", content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_list_profiles(self):
        response = self.client.get(self.url, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_patch_profile(self):
        response = self.client.patch(
            self.url + f"{self.test_profile.profile_id}/", self.data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_profile(self):
        response = self.client.put(
            self.url + f"{self.test_profile.profile_id}/", self.data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_profile(self):
        response = self.client.delete(self.url + f"{self.test_profile.profile_id}/", content_type="application/json")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


@override_settings(GOOGLE_API_KEY="Foo")
class TestGarden(TestCase):
    def setUp(self):
        self.url = "/garden/"
        profile = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})
        self.data = {"garden_name": "Foo", "direction": "north", "location": "Truro, UK",
                     "profile": str(profile.profile_id)}
        self.test_garden = create_test_garden()

        patcher = patch("geopy.geocoders.googlev3.GoogleV3.geocode",
                        return_value=Mock(**SAMPLE_GARDEN_GEOCODE_LOCATION))
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_create_garden(self):
        response = self.client.post(self.url, self.data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_delete_garden(self):
        response = self.client.delete(
            self.url + f"{self.test_garden.get('garden_id')}/", content_type="application/json")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_patch_garden(self):
        response = self.client.patch(
            self.url + f"{self.test_garden.get('garden_id')}/", self.data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_garden(self):
        response = self.client.put(
            self.url + f"{self.test_garden.get('garden_id')}/", self.data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class TestPlant(TestCase):
    def setUp(self):
        self.url = "/plant/"
        self.plant_data = SAMPLE_PLANT.copy()
        self.test_garden = Garden.objects.get(garden_id=create_test_garden().get("garden_id"))
        self.test_plant = Plant.objects.create(**self.plant_data, garden=self.test_garden)

        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = TREFLE_NAME_LOOKUP_RESPONSE
        mock_responses[1].json.return_value = TREFLE_ID_LOOKUP_RESPONSE

        patcher = patch("requests.get", side_effect=mock_responses)
        self.mock_get = patcher.start()
        self.addCleanup(patcher.stop)

    def test_create_plant(self):
        data = {
            "plant_name": "common woolly sunflower",
            "garden": self.test_garden.garden_id
        }
        response = self.client.post(self.url, data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_delete_plant(self):
        response = self.client.delete(
            self.url + f"{self.test_plant.plant_id}/", content_type="application/json")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_update_plant(self):
        response = self.client.put(
            self.url + f"{self.test_plant.plant_id}/", self.plant_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class TestRecommend(TestCase):
    def setUp(self):
        self.url = "/recommend/"
        self.test_garden = create_test_garden()
        self.plant_data = SAMPLE_PLANT.copy()

        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = TREFLE_NAME_LOOKUP_RESPONSE
        mock_responses[1].json.return_value = TREFLE_ID_LOOKUP_RESPONSE

        patcher = patch("requests.get", side_effect=mock_responses)
        self.mock_get = patcher.start()
        self.addCleanup(patcher.stop)

    def test_recommend_plants_for_garden(self):
        response = self.client.get(
            self.url + f"{self.test_garden.get('garden_id')}/?season=Spring", content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)