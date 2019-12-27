from rest_framework import viewsets, status
from rest_framework.response import Response

from encouragemint.encouragemint.models import Profile, Plant, Garden
from encouragemint.encouragemint.serializers import (
    ProfileSerializer, PlantSerializer, GardenSerializer,
    NewPlantRequestSerializer)
from encouragemint.lib.trefle.trefle import TrefleAPI
from encouragemint.lib.trefle.exceptions import TrefleConnectionError


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
    trefle = TrefleAPI()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NewPlantRequestSerializer
        return PlantSerializer

    def create(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        serializer = NewPlantRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plant_name_query = request.data["plant_name"]

        try:
            result = self._lookup_plant(plant_name_query, "common_name")
        except TrefleConnectionError:
            return Response(
                {"Message": "Encouragemint can't add new plants right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if not result:
            return Response(
                {"Message": "Encouragemint couldn't find any plants with that name."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if isinstance(result, dict):
            serializer = PlantSerializer(data=result)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(
            data=result,
            status=status.HTTP_300_MULTIPLE_CHOICES
        )

    def update(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        plant_id = kwargs["plant_id"]
        plant = Plant.objects.get(plant_id=plant_id)
        garden = plant.garden
        plant_name_query = plant.scientific_name

        try:
            result = self._lookup_plant(plant_name_query, "scientific_name", garden)
        except TrefleConnectionError:
            return Response(
                {"Message": "Encouragemint can't update plants right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = PlantSerializer(data=result)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def _lookup_plant(self, plant_name, query, garden=None):
        if query == "scientific_name":
            result = self.trefle.lookup_plants_by_scientific_name(plant_name)
        else:
            result = self.trefle.lookup_plants_by_expected_name(plant_name)

        if isinstance(result, dict):
            if not garden:
                garden = Garden.objects.get(garden_id=self.request.data["garden"])
            result["garden"] = garden.garden_id

        return result
