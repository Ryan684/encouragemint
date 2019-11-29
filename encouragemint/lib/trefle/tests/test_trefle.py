from django.test import TestCase

from encouragemint.lib.trefle.trefle import TrefleAPI


class TestTrefle(TestCase):
    def setUp(self):
        self.trefle = TrefleAPI()

    def test_lookup_plant_one_match(self):
        self.assertTrue(True)

    def test_lookup_plant_many_matches(self):
        self.assertTrue(True)

    def test_lookup_plant_no_matches(self):
        self.assertTrue(True)

    def test_lookup_plant_trefle_down(self):
        self.assertTrue(True)
