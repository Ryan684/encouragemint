from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

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


#  TODO: Fix tests
@api_view(["POST"])
def add_plant(request):
    try:
        assert "plant_name" in request.data
    except AssertionError:
        return Response(data={"message": "plant_name is a mandatory field."}, status=HTTP_400_BAD_REQUEST)
    try:
        assert "garden" in request.data
    except AssertionError:
        return Response(data={"message": "garden is a mandatory field."}, status=HTTP_400_BAD_REQUEST)

    plant = request.data.get("plant_name")
    data = TrefleAPI().lookup_plants_by_expected_name(plant)
    garden = Garden.objects.get(garden_id=request.data["garden"])
    data["garden"] = garden.garden_id
    serializer = PlantSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(data=data)
    return Response(data={"message": "Invalid Trefle data."}, status=HTTP_500_INTERNAL_SERVER_ERROR)
