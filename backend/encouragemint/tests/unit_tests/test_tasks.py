from unittest.mock import patch, ANY

from celery.exceptions import Retry
from django.test import TestCase

from backend.encouragemint.exceptions import GardenSystemError, GardenUserError
from backend.encouragemint.tasks import add_garden_location
from backend.encouragemint.tests.helpers import SAMPLE_GARDEN


class TestAddGardenLocation(TestCase):
    def setUp(self):
        self.garden_data = SAMPLE_GARDEN.copy()

        patcher = patch("backend.encouragemint.tasks.register_garden_coordinates")
        self.mock_register_garden_coordinates = patcher.start()
        self.addCleanup(patcher.stop)

    def test_successful_add_garden_location(self):
        self.mock_register_garden_coordinates.return_value = {}

        task = add_garden_location.s(self.garden_data).apply()

        self.assertEqual("SUCCESS", task.status)

    @patch("backend.encouragemint.tasks.add_garden_location.retry")
    def test_add_garden_location_retries_on_GardenSystemError_raise(self, mock_retry):
        self.mock_register_garden_coordinates.side_effect = error = GardenSystemError(None)
        mock_retry.side_effect = Retry

        self.assertRaises(Retry, add_garden_location, self.garden_data)
        mock_retry.assert_called_with(countdown=ANY, exc=error)

    def test_add_garden_location_raises_GardenUserError(self):
        self.mock_register_garden_coordinates.side_effect = GardenUserError(None)

        self.assertRaises(GardenUserError, add_garden_location, self.garden_data)
