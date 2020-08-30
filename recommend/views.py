import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger("django")


@api_view(["POST"])
def recommend(request):
    try:
        assert "season" in request.data
    except AssertionError:
        logger.info(
            f"Recommendation failed. The User did not supply a season query parameter.")
        return Response(
            {"message": "You must specify a season query parameter for plant recommendations."},
            status=status.HTTP_400_BAD_REQUEST
        )

    season = request.data["season"].upper()
    allowed_seasons = ["SPRING", "SUMMER", "AUTUMN", "WINTER"]

    try:
        assert season in allowed_seasons
    except AssertionError:
        logger.error(
            f"Recommendation failed. The user supplied an invalid season: {season}.")
        return Response(
            {"message": f"The season must be one of the following: {allowed_seasons}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if "duration" in request.data:
        allowed_durations = ["PERENNIAL", "ANNUAL", "BIENNIAL"]
        duration = request.data["duration"].upper()
        try:
            assert duration in allowed_durations
            duration = duration.lower().capitalize()
            # query["duration"] = duration
        except AssertionError:
            logger.error(f"Recommendation failed. User supplied invalid duration: {duration}.")
            return Response(
                {"message": f"The duration must be one of the following: {allowed_durations}"},
                status=status.HTTP_400_BAD_REQUEST
            )

    if "bloom_period" in request.data:
        allowed_bloom_periods = [
            f"EARLY {season}", f"MID {season}", f"{season}", f"LATE {season}"
        ]
        bloom_period = request.data["bloom_period"].upper()
        try:
            assert bloom_period in allowed_bloom_periods
           # query["bloom_period"] = bloom_period.lower().title()
        except AssertionError:
            logger.error(f"Recommendation failed. User supplied invalid bloom period: {bloom_period}.")
            return Response(
                {"message": f"The bloom_period must be one of the following: {allowed_bloom_periods}"},
                status=status.HTTP_400_BAD_REQUEST
            )
