class GeocoderConnectionError(Exception):
    def __init__(self):
        message = "Could not connect to the Google Geocoder API."
        super().__init__(message)
