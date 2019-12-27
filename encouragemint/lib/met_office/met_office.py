import geocoder
from django.conf import settings


class MetOfficeAPI:
    def print_geocode(self, location):
        g = geocoder.google(location, key=settings.GOOGLE_API_KEY)

        return g.latlng
