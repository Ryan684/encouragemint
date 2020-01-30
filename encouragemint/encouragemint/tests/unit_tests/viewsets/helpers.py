import json
from unittest.mock import patch, Mock

from django.test import override_settings
from rest_framework.test import APIRequestFactory

from encouragemint.encouragemint.models import Profile
from encouragemint.encouragemint.views import GardenViewSet

SAMPLE_GARDEN = {"garden_name": "Foo", "direction": "north", "location": "Truro, UK"}
SAMPLE_GARDEN_SUNLIGHT = "low"
SAMPLE_GARDEN_GEOCODE_LOCATION = {
    "address": SAMPLE_GARDEN.get("location"),
    "latitude": 50.263195,
    "longitude": -5.051041
}
SAMPLE_PLANT = {
    "scientific_name": "Eriophyllum lanatum",
    "common_name": "common woolly sunflower",
    "duration": "Annual, Perennial",
    "bloom_period": "Spring",
    "growth_period": "Summer",
    "growth_rate": "Slow",
    "shade_tolerance": "High",
    "moisture_use": "High",
    "family_common_name": "Aster family",
    "trefle_id": 134845
}


@override_settings(GOOGLE_API_KEY="Foo")
@patch("geopy.geocoders.googlev3.GoogleV3.geocode")
def create_test_garden(mock_google):
    profile = Profile.objects.create(**{"first_name": "Foo", "last_name": "Bar"})
    garden = {"garden_name": "Foo", "direction": "north", "location": "Truro, UK",
              "profile": str(profile.profile_id)}
    mock = Mock(**{
        "address": garden.get("location"),
        "latitude": 50.263195,
        "longitude": -5.051041
    })
    mock_google.return_value = mock

    request = APIRequestFactory().post(
        "/garden/",
        garden,
        format="json"
    )
    view = GardenViewSet.as_view({"post": "create"})
    response = view(request)
    response.render()
    model_data = json.loads(response.content.decode("utf-8"))
    return model_data
