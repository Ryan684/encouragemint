from rest_framework import viewsets

from encouragemint.encouragemint.models.profile import Profile
from encouragemint.encouragemint.notifications.email import send_profile_created_email
from encouragemint.encouragemint.serializers.profile_serializer import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "profile_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def perform_create(self, serializer):
        new_user = serializer.save()
        send_profile_created_email(new_user.email_address, new_user.first_name)
