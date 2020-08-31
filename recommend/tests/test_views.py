from django.test import TestCase
from rest_framework.test import APIRequestFactory


class TestRecommend(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
       # self.view = recommend
        self.recommend_url = "/recommend/"

    def test_invalid_input(self):
        pass

    def test_valid_task_call(self):
        pass
