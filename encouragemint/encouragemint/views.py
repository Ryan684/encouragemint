from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

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

    def create(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        new_plant = self._lookup_plant()
        serializer = PlantSerializer(data=new_plant)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def _lookup_plant(self):
        plant_name_query = self.request.data.get("plant_name")
        matched_plant = TrefleAPI().lookup_plants_by_expected_name(plant_name_query)
        garden = Garden.objects.get(garden_id=self.request.data["garden"])
        matched_plant["garden"] = garden.garden_id
        return matched_plant
