import logging

from rest_framework import views, status
from rest_framework.response import Response

from recommend.recommender import recommend_plants
from recommend.serializers import RecommendSerializer

logger = logging.getLogger("django")


class RecommendView(views.APIView):
    def post(self, request):
        serializer = RecommendSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            results = recommend_plants(serializer.data)
            return Response(results, status.HTTP_200_OK)
