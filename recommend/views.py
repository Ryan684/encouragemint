import logging

from rest_framework import views, status
from rest_framework.response import Response

from recommend.serializers import RecommendSerializer
from recommend.tasks import execute_recommendation

logger = logging.getLogger("django")


class RecommendView(views.APIView):
    def post(self, request):
        serializer = RecommendSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            execute_recommendation.s().delay()
            return Response({"Processing.."}, status=status.HTTP_202_ACCEPTED)
