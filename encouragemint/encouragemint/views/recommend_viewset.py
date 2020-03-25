import logging

from rest_framework import generics, status
from rest_framework.response import Response

from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.weather import get_garden_moisture
from encouragemint.interfaces.trefle.exceptions import TrefleConnectionError
from encouragemint.interfaces.trefle.trefle import lookup_plants

logger = logging.getLogger("django")


class RecommendViewSet(generics.RetrieveAPIView):
    queryset = Garden.objects.all()
    lookup_field = "garden_id"
    http_method_names = ["get"]

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

        return self._recommend_plants(query, garden)

    def _recommend_plants(self, query, garden):  # pylint: disable=no-self-use
        try:
            plants = lookup_plants(query)
        except TrefleConnectionError as exception:
            logger.error(f"Recommendation failed for garden {garden.garden_id}: {exception}")
            return Response(
                {"Message": "Encouragemint can't recommend plants for your garden right now. "
                            "Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        logger.info(
            f"{len(plants)} plants matched the search criteria {query} "
            f"for garden {garden.garden_id}.")
        return Response(plants, status=status.HTTP_200_OK)
