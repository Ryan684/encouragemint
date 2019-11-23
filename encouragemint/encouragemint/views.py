from rest_framework import viewsets

from encouragemint.encouragemint.models import Profile, Plant
from encouragemint.encouragemint.serializers import ProfileSerializer, PlantSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by("-id")
    serializer_class = ProfileSerializer
    lookup_field = "profile_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all().order_by("-id")
    serializer_class = PlantSerializer
    lookup_field = "plant_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]