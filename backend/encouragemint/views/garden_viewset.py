import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.encouragemint.models.garden import Garden
from backend.encouragemint.serializers.garden_serializer import GardenSerializer
from backend.encouragemint.tasks import add_garden_location
from backend.encouragemint.weather import get_garden_moisture
from backend.interfaces.trefle.exceptions import TrefleConnectionError
from backend.interfaces.trefle.trefle import lookup_plants

logger = logging.getLogger("django")


class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    lookup_field = "garden_id"
    http_method_names = ["get", "post", "patch", "delete"]

    def perform_create(self, serializer):  # pylint: disable=no-self-use
        garden_data = serializer.save()
        logger.info(f"Garden {garden_data.garden_id} has been created and added to "
                    f"profile {garden_data.profile.profile_id}.")
        add_garden_location.delay(garden_data.garden_id)

    def perform_update(self, serializer):
        garden_data = serializer.save()
        logger.info(f"Updated garden {garden_data.garden_id} with the following data: "
                    f"{self.request.data}")
        add_garden_location.delay(garden_data.garden_id)

    @action(detail=True, methods=["get"])
    def recommend(self, request, garden_id=None):
        garden = self.get_object()

        try:
            assert "season" in request.GET
        except AssertionError:
            logger.info(
                f"Recommendation failed for garden {garden_id}: "
                "User did not supply a season query parameter.")
            return Response(
                {"message": "You must specify a season query parameter for plant recommendations."},
                status=status.HTTP_400_BAD_REQUEST
            )

        season = request.GET["season"].upper()
        allowed_seasons = ["SPRING", "SUMMER", "AUTUMN", "WINTER"]

        try:
            assert season in allowed_seasons
        except AssertionError:
            logger.error(
                f"Recommendation failed for garden {garden_id}: "
                f"User supplied an invalid season: {season}.")
            return Response(
                {"message": "The season must be one of the following: "
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
                logger.error(f"Recommendation failed for garden {garden_id}: "
                             f"User supplied invalid duration: {duration}.")
                return Response(
                    {"message": "The duration must be one of the following: "
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
                logger.error(f"Recommendation failed for garden {garden_id}: "
                             f"User supplied invalid bloom period: {bloom_period}.")
                return Response(
                    {"message": "The bloom_period must be one of the following: "
                                f"{allowed_bloom_periods}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return self._recommend_plants(query, garden)

    def _recommend_plants(self, query, garden):  # pylint: disable=no-self-use
        try:
            plants = lookup_plants(query)
        except TrefleConnectionError as exception:
            logger.error(f"Recommendation failed for garden {garden.garden_id}: {exception}")
            return Response(
                {"message": "Encouragemint can't recommend plants for your garden right now. "
                            "Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        number_of_records_returned = (len(plants) if len(plants) != 100 else "100+")
        logger.info(
            f"{number_of_records_returned} plants matched the search criteria {query} "
            f"for garden {garden.garden_id}.")
        return Response(plants, status=status.HTTP_200_OK)
