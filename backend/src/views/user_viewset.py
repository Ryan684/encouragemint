from django.contrib.auth.models import User
from rest_framework import viewsets

from backend.src.notifications.email import send_user_created_email
from backend.src.serializers.user_serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def perform_create(self, serializer):  # pylint: disable=no-self-use
        new_user = serializer.save()
        send_user_created_email(new_user.email, new_user.first_name)
