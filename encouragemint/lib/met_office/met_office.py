import geocoder
from django.conf import settings


class MetOfficeAPI:
    def _geocode_location(self, location):
        geocode = geocoder.google(location, key=settings.GOOGLE_API_KEY)

        return geocode.latlng
