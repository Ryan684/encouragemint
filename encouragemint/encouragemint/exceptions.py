class GeocoderConnectionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class GeocoderNoResultsError(Exception):
    pass
