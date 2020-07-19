import json
import logging

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger("django")


@api_view(["POST"])
def login(request):
    try:
        assert "username" in request.data
    except AssertionError:
        logger.info(
            "User login failed. User did not supply a username parameter.")
        return Response(
            {"message": "You must specify a username parameter to login."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        assert "password" in request.data
    except AssertionError:
        logger.info(
            "User login failed. User did not supply a password parameter.")
        return Response(
            {"message": "You must specify a password parameter to login."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=request.data["username"], password=request.data["password"])

    if user is not None:
        return Response(
            {"message": "login successful"},
            status=status.HTTP_200_OK
        )

    return Response(
        {"message": "login failed"},
        status=status.HTTP_400_BAD_REQUEST
    )
