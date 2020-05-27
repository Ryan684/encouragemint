from rest_framework import viewsets

from backend.src.models.profile import Profile
from backend.src.notifications.email import send_profile_created_email
from backend.src.serializers.profile_serializer import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "profile_id"
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def perform_create(self, serializer):  # pylint: disable=no-self-use
        new_user = serializer.save()
        send_profile_created_email(new_user.email_address, new_user.first_name)
