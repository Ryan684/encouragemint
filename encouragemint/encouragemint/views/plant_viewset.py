import logging

from rest_framework import viewsets, status
from rest_framework.response import Response

from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.models.plant import Plant
from encouragemint.encouragemint.serializers.new_plant_request_serializer import \
    NewPlantRequestSerializer
from encouragemint.encouragemint.serializers.plant_serializer import PlantSerializer
from encouragemint.interfaces.trefle.exceptions import TrefleConnectionError
from encouragemint.interfaces.trefle.trefle import lookup_plants

logger = logging.getLogger("django")


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    lookup_field = "plant_id"
    http_method_names = ["post", "put", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return NewPlantRequestSerializer
        return PlantSerializer

    def create(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        serializer = NewPlantRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plant_name = request.data["plant_name"]
        garden = Garden.objects.get(garden_id=request.data["garden"])

        try:
            result = self._lookup_plant_by_name(plant_name, garden)
        except TrefleConnectionError as exception:
            logger.error(f"Adding plant failed for garden {garden.garden_id}: {exception}")
            return Response(
                {"Message": "Encouragemint can't add new plants right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if not result:
            logger.error(
                f"Adding plant failed for garden {garden.garden_id}: "
                f"No plants found for {plant_name}.")
            return Response(
                {"Message": "Encouragemint couldn't find any plants with that name."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if isinstance(result, dict):
            serializer = PlantSerializer(data=result)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            logger.info(
                f"Added plant {serializer.data['plant_id']} "
                f"to garden {garden.garden_id} successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(
            data=result,
            status=status.HTTP_300_MULTIPLE_CHOICES
        )

    def update(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        plant_id = kwargs["plant_id"]
        plant = Plant.objects.get(plant_id=plant_id)
        garden = plant.garden
        plant_name = plant.scientific_name

        try:
            result = self._lookup_plant_by_name(plant_name, garden)
        except TrefleConnectionError as exception:
            logger.error(f"Update failed for plant {plant} in garden {garden}: {exception}")
            return Response(
                {"Message": "Encouragemint can't update plants right now. Try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = PlantSerializer(data=result)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        logger.info(f"Updated plant {plant} in garden {garden} successfully.")
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def _lookup_plant_by_name(self, plant_name, garden):  # pylint: disable=no-self-use
        formatted_plant_name = plant_name.lower().capitalize()
        result = lookup_plants({"scientific_name": formatted_plant_name})

        if isinstance(result, dict):
            result["garden"] = garden.garden_id

        return result
