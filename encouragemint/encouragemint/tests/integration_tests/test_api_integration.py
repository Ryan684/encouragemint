from django.test import TestCase

from rest_framework import status

from encouragemint.encouragemint.models import Profile


class TestProfile(TestCase):
    def setUp(self):
        self.url = "/profile/"
        self.data = {"first_name": "Foo", "last_name": "Bar"}
        self.test_profile = Profile.objects.create(**self.data)

    def test_create_profile(self):
        response = self.client.post(self.url, self.data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_retrieve_profile(self):
        response = self.client.get(self.url + f"{self.test_profile.profile_id}/", content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_list_profiles(self):
        response = self.client.get(self.url, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_patch_profile(self):
        response = self.client.patch(
            self.url + f"{self.test_profile.profile_id}/", self.data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_update_profile(self):
        response = self.client.put(
            self.url + f"{self.test_profile.profile_id}/", self.data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_profile(self):
        response = self.client.delete(self.url + f"{self.test_profile.profile_id}/", content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)


# class TestGarden(TestCase):
#     def setUp(self):
#         self.url = "/garden/"
#         self.data = {
#
#         }
#
#     def test_create_garden(self):
#         response = self.client.post(self.url, self.data, format="json")
#         self.assertEqual(status.HTTP_201_CREATED, response.status_code)
#
#     def test_delete_garden(self):
#         response = self.client.post(self.url, self.data, format="json")
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#
#     def test_patch_garden(self):
#         response = self.client.post(self.url, self.data, format="json")
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#
#     def test_update_garden(self):
#         response = self.client.post(self.url, self.data, format="json")
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#
#
# class TestPlant(TestCase):
#     def setUp(self):
#         self.url = "/plant/"
#         self.data = {
#
#         }
#
#     def test_create_plant(self):
#         response = self.client.post(self.url, self.data, format="json")
#         self.assertEqual(status.HTTP_201_CREATED, response.status_code)
#
#     def test_delete_plant(self):
#         response = self.client.post(self.url, self.data, format="json")
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#
#     def test_update_garden(self):
#         response = self.client.post(self.url, self.data, format="json")
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
