import logging

from rest_framework import viewsets

from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.serializers.garden_serializer import GardenSerializer
from encouragemint.encouragemint.tasks import add_garden_location

logger = logging.getLogger("django")


class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    lookup_field = "garden_id"
    http_method_names = ["post", "put", "patch", "delete"]

    def perform_create(self, serializer):
        garden_data = serializer.save()
        logger.info(f"Garden {garden_data.garden_id} has been created and added to "
                    f"profile {garden_data.profile.profile_id}.")
        add_garden_location.delay(garden_data.garden_id)
