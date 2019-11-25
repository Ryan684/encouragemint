from rest_framework import viewsets

from encouragemint.encouragemint.models import Profile, Plant, Garden
from encouragemint.encouragemint.serializers import ProfileSerializer, PlantSerializer, GardenSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "profile_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]


class GardenViewSet(viewsets.ModelViewSet):
    queryset = Garden.objects.all()
    serializer_class = GardenSerializer
    lookup_field = "garden_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    lookup_field = "plant_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]
