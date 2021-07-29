import logging

import requests
from rest_framework import views, status
from rest_framework.response import Response

from backend.exceptions import GeocoderNoResultsError
from backend.recommender import recommend_plants
from backend.serializers import RecommendSerializer

logger = logging.getLogger("django")


class RecommendView(views.APIView):
    def post(self, request):  # pylint: disable=no-self-use
        serializer = RecommendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            results = recommend_plants(serializer.validated_data)
        except requests.exceptions.RequestException:
            return Response(
                {"message":
                 "We're unable to recommend plants for you right now, try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except GeocoderNoResultsError:
            return Response(
                {"message":
                 "We couldn't find your location. Please try and be more specific."},
                status=status.HTTP_400_BAD_REQUEST)

        logger.warning(results)
        return Response(results, status=status.HTTP_200_OK)
