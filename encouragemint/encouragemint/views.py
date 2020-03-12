import logging

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
from encouragemint.encouragemint.weather import get_garden_moisture
from encouragemint.interfaces.meteostat.meteostat import MeteostatAPI
from encouragemint.interfaces.trefle.trefle import TrefleAPI
from encouragemint.interfaces.trefle.exceptions import TrefleConnectionError

TREFLE = TrefleAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "profile_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]


class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    lookup_field = "garden_id"
    http_method_names = ["post", "put", "patch", "delete"]

    def create(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_create(serializer)

    def perform_create(self, serializer):
        profile = self.request.data["profile"]
        try:
            latitude, longitude, location = self._lookup_garden_coordinates()
        except GeocoderConnectionError as exception:
            logger.error(f"Adding garden failed for profile {profile}: {exception}")
            return Response(
                {"Message": "Encouragemint can't create new gardens right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except GeocoderNoResultsError:
            logger.error(
                f"Adding garden failed for profile {profile}. "
                "Could not find a location for that address.")
            return Response(
                {"Message": "Encouragemint couldn't find that location. Try to be more accurate."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(latitude=latitude, longitude=longitude, location=location)
        headers = self.get_success_headers(serializer.data)
        logger.info(
            f"Added garden {serializer.data['garden_id']} to profile {profile} successfully.")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _lookup_garden_coordinates(self):
        try:
            geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY)
            location = geolocator.geocode(self.request.data["location"])

            if location:
                return location.latitude, location.longitude, location.address
            raise GeocoderNoResultsError()
        except GeopyError as exception:
            raise GeocoderConnectionError(exception)


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    lookup_field = "plant_id"
    http_method_names = ["post", "put", "delete"]

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
        except TrefleConnectionError as exception:
            logger.error(f"Adding plant failed for garden {garden.garden_id}: {exception}")
            return Response(
                {"Message": "Encouragemint can't add new plants right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if not result:
            logger.error(
                f"Adding plant failed for garden {garden.garden_id}: "
                f"No plants found for {plant_name}.")
            return Response(
                {"Message": "Encouragemint couldn't find any plants with that name."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if isinstance(result, dict):
            serializer = PlantSerializer(data=result)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info(
                f"Added plant {serializer.data['plant_id']} to garden {garden.garden_id} successfully.")
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
        except TrefleConnectionError as exception:
            logger.error(f"Update failed for plant {plant} in garden {garden}: {exception}")
            return Response(
                {"Message": "Encouragemint can't update plants right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = PlantSerializer(data=result)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"Updated plant {plant} in garden {garden} successfully.")
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def _lookup_plant_by_name(self, query, plant_name, garden):  # pylint: disable=no-self-use
        result = TREFLE.lookup_plants({query: plant_name})

        if isinstance(result, dict):
            result["garden"] = garden.garden_id

        return result


class RecommendViewSet(generics.RetrieveAPIView):
    queryset = Garden.objects.all()
    lookup_field = "garden_id"
    http_method_names = ["get"]
    meteostat = MeteostatAPI()

    def retrieve(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        garden = self.get_object()

        try:
            assert "season" in request.GET
        except AssertionError:
            logger.info(
                f"Recommendation failed for garden {garden.garden_id}: "
                "User did not supply a season parameter.")
            return Response(
                {"Message": "You must specify a season url parameter for plant recommendations."},
                status=status.HTTP_400_BAD_REQUEST
            )

        season = request.GET["season"].upper()
        allowed_seasons = ["SPRING", "SUMMER", "AUTUMN", "WINTER"]

        try:
            assert season in allowed_seasons
        except AssertionError:
            logger.error(
                f"Recommendation failed for garden {garden.garden_id}: "
                f"User supplied an invalid season: {season}.")
            return Response(
                {"Message": "The season parameter must be one of the following: "
                            f"{allowed_seasons}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        query = {"shade_tolerance": garden.shade_tolerance}
        moisture_use = get_garden_moisture(garden, season)

        if moisture_use:
            query["moisture_use"] = moisture_use

        if "duration" in request.GET:
            allowed_durations = ["PERENNIAL", "ANNUAL", "BIENNIAL"]
            duration = request.GET["duration"].upper()
            try:
                assert duration in allowed_durations
                duration = duration.lower().capitalize()
                query["duration"] = duration
            except AssertionError:
                logger.error(f"Recommendation failed for garden {garden.garden_id}: "
                             f"User supplied invalid duration: {duration}.")
                return Response(
                    {"Message": "The duration must be one of the following: "
                                f"{allowed_durations}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if "bloom_period" in request.GET:
            allowed_bloom_periods = [
                f"EARLY {season}", f"MID {season}", f"{season}", f"LATE {season}"
            ]
            bloom_period = request.GET["bloom_period"].upper()
            try:
                assert bloom_period in allowed_bloom_periods
                query["bloom_period"] = bloom_period.lower().title()
            except AssertionError:
                logger.error(f"Recommendation failed for garden {garden.garden_id}: "
                             f"User supplied invalid bloom period: {bloom_period}.")
                return Response(
                    {"Message": "The bloom_period must be one of the following: "
                                f"{allowed_bloom_periods}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return self.recommend_plants(query, garden)

    def recommend_plants(self, query, garden):  # pylint: disable=no-self-use
        try:
            plants = TREFLE.lookup_plants(query)
        except TrefleConnectionError as exception:
            logger.error(f"Recommendation failed for garden {garden.garden_id}: {exception}")
            return Response(
                {"Message": "Encouragemint can't recommend plants for your garden right now. "
                            "Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        logger.info(
            f"{len(plants)} plants matched the search criteria {query} for garden {garden.garden_id}.")
        return Response(plants, status=status.HTTP_200_OK)
