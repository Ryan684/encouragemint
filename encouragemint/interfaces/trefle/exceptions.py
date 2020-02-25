class TrefleConnectionError(Exception):
    def __init__(self):
        message = "Could not connect to the Trefle API."
        super().__init__(message)
