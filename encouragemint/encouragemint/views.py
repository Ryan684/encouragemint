from django.conf import settings
from geopy import GoogleV3
from geopy.exc import GeopyError
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from encouragemint.encouragemint.exceptions import GeocoderConnectionError, GeocoderNoResultsError
from encouragemint.encouragemint.models import Profile, Plant, Garden
from encouragemint.encouragemint.serializers import (
    ProfileSerializer, PlantSerializer, GardenSerializer,
    NewPlantRequestSerializer)
from encouragemint.lib import trefle
from encouragemint.lib.trefle.trefle import TrefleAPI
from encouragemint.lib.trefle.exceptions import TrefleConnectionError

TREFLE = TrefleAPI()


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

    def create(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)

    def perform_create(self, serializer):
        try:
            latitude, longitude, location = self._lookup_garden_coordinates()
        except GeocoderConnectionError:
            return Response(
                {"Message": "Encouragemint can't create new gardens right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except GeocoderNoResultsError:
            return Response(
                {"Message": "Encouragemint couldn't find that location. Try to be more accurate."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(latitude=latitude, longitude=longitude, location=location)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _lookup_garden_coordinates(self):
        try:
            geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY)
            location = geolocator.geocode(self.request.data["location"])

            if location:
                return location.latitude, location.longitude, location.address
            raise GeocoderNoResultsError()
        except GeopyError:
            raise GeocoderConnectionError()


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
        plant_name = request.data["plant_name"]
        garden = Garden.objects.get(garden_id=self.request.data["garden"])

        try:
            result = self._lookup_plant_by_name("common_name", plant_name, garden)
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
        plant_name = plant.scientific_name

        try:
            result = self._lookup_plant_by_name("scientific_name", plant_name, garden)
        except trefle.exceptions.TrefleConnectionError:
            return Response(
                {"Message": "Encouragemint can't update plants right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = PlantSerializer(data=result)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def _lookup_plant_by_name(self, query, plant_name, garden):
        result = TREFLE.lookup_plants({query: plant_name})

        if isinstance(result, dict):
            result["garden"] = garden.garden_id

        return result


class RecommendViewSet(generics.RetrieveAPIView):
    queryset = Garden.objects.all()
    lookup_field = "garden_id"
    http_method_names = ["get"]

    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        garden = self.get_object()
        query = {"shade_tolerance": self._get_shade_tolerance(garden)}

        try:
            plants = TREFLE.lookup_plants(query)
        except trefle.exceptions.TrefleConnectionError:
            return Response(
                {"Message": "Encouragemint can't recommend plants for your garden right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(plants)

    def _get_shade_tolerance(self, garden):  # pylint: disable=no-self-use
        if garden.sunlight == "north":
            return "Tolerant"
        if garden.sunlight == "south":
            return "Intolerant"
        return "Intermediate"
