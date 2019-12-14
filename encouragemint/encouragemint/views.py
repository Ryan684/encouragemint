from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from encouragemint.encouragemint.models import Profile, Plant, Garden
from encouragemint.encouragemint.serializers import (
    ProfileSerializer, PlantSerializer, GardenSerializer,
    NewPlantRequestSerializer)
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
    lookup_field = "plant_id"
    http_method_names = ["get", "post", "put", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NewPlantRequestSerializer
        return PlantSerializer

    def perform_create(self, serializer):
        new_plant = self._add_plant()
        plant_serializer = PlantSerializer(data=new_plant.data)

        if plant_serializer.is_valid():
            plant_serializer.save()

    def _add_plant(self):
        plant = self.request.data.get("plant_name")
        data = TrefleAPI().lookup_plants_by_expected_name(plant)
        garden = Garden.objects.get(garden_id=self.request.data["garden"])
        data["garden"] = garden.garden_id
        return Response(
            data=data,
            status=HTTP_200_OK
        )

