from rest_framework import viewsets

from encouragemint.models import Profile
from encouragemint.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by("-id")
    serializer_class = ProfileSerializer
    lookup_field = "profile_id"
