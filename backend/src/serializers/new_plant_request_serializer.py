import re

from rest_framework import serializers


class NewPlantRequestSerializer(serializers.Serializer):
    plant_name = serializers.CharField(max_length=50)
    garden = serializers.UUIDField()

    @staticmethod
    def validate_plant_name(value):
        if re.fullmatch(r"^[a-zA-Z\-\s']+$", value) is None:
            raise serializers.ValidationError(
                "Invalid entry for the plant's's name. A garden's name can only "
                "contain letters, hyphens, spaces and apostrophes.")
        return value
