import logging

from rest_framework import status
from rest_framework.response import Response

from encouragemint.encouragemint.exceptions import GardenUserError, GardenSystemError
from encouragemint.encouragemint.garden import create_garden

logger = logging.getLogger("django")


def add_garden(garden_data):
    try:
        return create_garden(garden_data)
    except GardenSystemError as exception:
        logger.error(exception)
        return Response(
            {"Message": "Encouragemint can't create new gardens right now. Try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except GardenUserError as exception:
        logger.error(exception)
        return Response(
            {"Message": "Encouragemint couldn't find that location. Try to be more accurate."},
            status=status.HTTP_400_BAD_REQUEST
        )
