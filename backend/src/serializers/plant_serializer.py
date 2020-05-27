from rest_framework import serializers

from backend.src.models.garden import Garden
from backend.src.models.plant import Plant


class PlantSerializer(serializers.ModelSerializer):
    garden = serializers.SlugRelatedField(slug_field="garden_id", queryset=Garden.objects.all())

    class Meta:
        model = Plant
        fields = ["plant_id", "garden", "common_name", "trefle_id", "scientific_name",
                  "duration", "bloom_period", "growth_period", "growth_rate",
                  "shade_tolerance", "moisture_use", "family_common_name"]
        read_only_fields = ["plant_id", "garden"]
