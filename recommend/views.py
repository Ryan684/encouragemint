import logging

from rest_framework import views, status
from rest_framework.response import Response

from backend.interfaces.meteostat.exceptions import MeteostatConnectionError
from backend.interfaces.trefle.exceptions import TrefleConnectionError
from recommend.exceptions import GeocoderNoResultsError
from recommend.recommender import recommend_plants
from recommend.serializers import RecommendSerializer

logger = logging.getLogger("django")


class RecommendView(views.APIView):
    def post(self, request):
        serializer = RecommendSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                results = recommend_plants(serializer.validated_data)
            except (TrefleConnectionError, MeteostatConnectionError):
                return Response(
                    {"message": "We're unable to recommend plants for you right now, try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except GeocoderNoResultsError:
                return Response(
                    {"message": "We couldn't find your location. Please try and be more specific."},
                    status=status.HTTP_400_BAD_REQUEST)

            return Response(results, status=status.HTTP_200_OK)
