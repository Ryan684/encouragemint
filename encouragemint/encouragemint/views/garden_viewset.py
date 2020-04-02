import logging

from django.conf import settings
from geopy import GoogleV3
from geopy.exc import GeopyError
from rest_framework import viewsets, status
from rest_framework.response import Response

from encouragemint.encouragemint.exceptions import GeocoderConnectionError, GeocoderNoResultsError
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
        return self.perform_create(serializer)

    def perform_create(self, serializer):
        profile = self.request.data["profile"]
        try:
            latitude, longitude, location = self._lookup_garden_coordinates()
        except GeocoderConnectionError as exception:
            logger.error(f"Adding garden failed for profile {profile}: {exception}")
            return Response(
                {"Message": "Encouragemint can't create new gardens right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except GeocoderNoResultsError:
            logger.error(
                f"Adding garden failed for profile {profile}. "
                "Could not find a location for that address.")
            return Response(
                {"Message": "Encouragemint couldn't find that location. Try to be more accurate."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(latitude=latitude, longitude=longitude, location=location)
        headers = self.get_success_headers(serializer.data)
        logger.info(
            f"Added garden {serializer.data['garden_id']} to profile {profile} successfully.")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _lookup_garden_coordinates(self):
        try:
            geolocator = GoogleV3(api_key=settings.GOOGLE_API_KEY)
            location = geolocator.geocode(self.request.data["location"])

            if location:
                return location.latitude, location.longitude, location.address
            raise GeocoderNoResultsError()
        except GeopyError as exception:
            raise GeocoderConnectionError(exception)
