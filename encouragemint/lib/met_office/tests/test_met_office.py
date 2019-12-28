from unittest.mock import patch, Mock

from django.test import TestCase, override_settings

from encouragemint.lib.met_office.met_office import MetOfficeAPI


@override_settings(GOOGLE_API_KEY="Foo")
class TestMetOfficeAPI(TestCase):
    def setUp(self):
        self.met_office = MetOfficeAPI()

    @patch("geocoder.google")
    def test_print_geocode(self, mock_google):
        expected_latlng = [50.263195, -5.051041]
        mock = Mock()
        mock.latlng = expected_latlng
        mock_google.return_value = mock

        self.assertEqual(expected_latlng, self.met_office._geocode_location("Truro, UK"))
