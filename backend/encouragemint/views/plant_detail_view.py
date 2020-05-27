import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.interfaces.trefle.exceptions import TrefleConnectionError
from backend.interfaces.trefle.trefle import lookup_plant_by_id

logger = logging.getLogger("django")


@api_view(["GET"])
def plant_detail(request, **kwargs):  # pylint: disable=unused-argument
    try:
        assert "trefle_id" in kwargs
    except AssertionError:
        logger.info(
            "Plant detail lookup failed. User did not supply a trefle_id path parameter.")
        return Response(
            {"message": "You must specify a trefle_id path parameter for plant details."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        plant = lookup_plant_by_id(kwargs["trefle_id"])
    except TrefleConnectionError:
        return Response(
            {"message": "Encouragemint can't find details on this plant right now. "
                        "Try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    if not plant:
        return Response(
            {"message": "no plants could be found for this trefle_id."},
            status=status.HTTP_200_OK)

    plant_details = {
        "scientific_name": plant.get("scientific_name"),
        "common_name": plant.get("common_name"),
        "images": plant.get("images")
    }

    return Response(plant_details, status=status.HTTP_200_OK)
