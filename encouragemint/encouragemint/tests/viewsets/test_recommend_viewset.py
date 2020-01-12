from django.test import TestCase

from encouragemint.encouragemint.views import RecommendViewSet

# Test /recommend with
#     - each shade tolerance scenario
#     - trefle exceptions thrown

class TestGardenViewsetParameters(TestCase):
    def test_viewset_parameters(self):
        self.assertEqual(["get"], RecommendViewSet.http_method_names)
        self.assertEqual("garden_id", RecommendViewSet.lookup_field)
