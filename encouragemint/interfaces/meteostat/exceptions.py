class MeteostatConnectionError(Exception):
    def __init__(self):
        message = "Could not connect to the Meteostat API."
        super().__init__(message)
