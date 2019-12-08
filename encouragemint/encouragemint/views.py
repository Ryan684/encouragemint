from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from encouragemint.encouragemint.models import Profile, Plant, Garden
from encouragemint.encouragemint.serializers import (
    ProfileSerializer, PlantSerializer, GardenSerializer
)
from encouragemint.lib.trefle.trefle import TrefleAPI


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "profile_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]


class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    lookup_field = "garden_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    lookup_field = "plant_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]


#  TODO: Find best practice here
@api_view(["POST"])
def add_plant(request):
    assert "plant_name" in request.data
    assert "garden" in request.data
    plant = request.data.get("plant_name")
    data = TrefleAPI().lookup_plants_by_expected_name(plant)
    return Response(data=data)
