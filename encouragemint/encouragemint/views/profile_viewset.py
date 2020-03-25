from rest_framework import viewsets

from encouragemint.encouragemint.models.profile import Profile
from encouragemint.encouragemint.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "profile_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]
