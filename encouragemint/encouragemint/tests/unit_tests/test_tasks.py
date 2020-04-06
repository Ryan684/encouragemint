from unittest.mock import patch, ANY

from celery.exceptions import Retry
from django.test import TestCase

from encouragemint.encouragemint.exceptions import GardenSystemError, GardenUserError
from encouragemint.encouragemint.tasks import add_garden
from encouragemint.encouragemint.tests.helpers import SAMPLE_GARDEN


class TestAddGarden(TestCase):
    def setUp(self):
        self.garden_data = SAMPLE_GARDEN.copy()

        patcher = patch("encouragemint.encouragemint.tasks.create_garden")
        self.mock_google = patcher.start()
        self.addCleanup(patcher.stop)

    def test_successful_add_garden(self):
        self.mock_google.return_value = {}

        task = add_garden.s(self.garden_data).apply()

        self.assertEqual("SUCCESS", task.status)

    @patch("encouragemint.encouragemint.tasks.add_garden.retry")
    def test_add_garden_retries_on_GardenSystemError_raise(self, mock_retry):
        self.mock_google.side_effect = error = GardenSystemError(None)
        mock_retry.side_effect = Retry

        self.assertRaises(Retry, add_garden, self.garden_data)
        mock_retry.assert_called_with(countdown=ANY, exc=error)

    def test_add_garden_raises_GardenUserError(self):
        self.mock_google.side_effect = GardenUserError(None)

        self.assertRaises(GardenUserError, add_garden, self.garden_data)
