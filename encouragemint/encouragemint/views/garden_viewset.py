import logging

from rest_framework import viewsets

from encouragemint.encouragemint.garden import create_garden
from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.serializers.garden_serializer import GardenSerializer

logger = logging.getLogger("django")


class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    lookup_field = "garden_id"
    http_method_names = ["post", "put", "patch", "delete"]

    def create(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return create_garden(self.request.data)
