class TrefleConnectionError(Exception):
    def __init__(self, error):
        message = "Could not connect to the Trefle API - {}".format(error)

        super().__init__(message)
