import re

from rest_framework import serializers

from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.models.plant import Plant


class PlantSerializer(serializers.ModelSerializer):
    garden = serializers.SlugRelatedField(slug_field="garden_id", queryset=Garden.objects.all())

    class Meta:
        model = Plant
        fields = ["plant_id", "garden", "common_name", "trefle_id", "scientific_name",
                  "duration", "bloom_period", "growth_period", "growth_rate",
                  "shade_tolerance", "moisture_use", "family_common_name"]
        read_only_fields = ["plant_id", "garden"]

    @staticmethod
    def validate_scientific_name(value):
        if re.fullmatch(r"^[a-zA-Z\-\s.']+$", value) is None:
            raise serializers.ValidationError(
                "Invalid entry for the plant's scientific name.")
        return value

    @staticmethod
    def validate_duration(value):
        if value:
            if re.fullmatch(r"^[a-zA-Z,\s]+$", value) is None:
                raise serializers.ValidationError(
                    "Invalid entry for the plant's duration.")
        return value

    @staticmethod
    def validate_bloom_period(value):
        if value:
            if re.fullmatch(r"^[a-zA-Z\s,]+$", value) is None:
                raise serializers.ValidationError(
                    "Invalid entry for the plant's bloom period.")
        return value

    @staticmethod
    def validate_growth_period(value):
        if value:
            if re.fullmatch(r"^[a-zA-Z\s,]+$", value) is None:
                raise serializers.ValidationError(
                    "Invalid entry for the plant's growth period.")
        return value

    @staticmethod
    def validate_growth_rate(value):
        if value:
            if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
                raise serializers.ValidationError(
                    "Invalid entry for the plant's growth rate.")
        return value

    @staticmethod
    def validate_shade_tolerance(value):
        if value:
            if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
                raise serializers.ValidationError(
                    "Invalid entry for the plant's shade tolerance.")
        return value

    @staticmethod
    def validate_moisture_use(value):
        if value:
            if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
                raise serializers.ValidationError(
                    "Invalid entry for the plant's moisture use.")
        return value

    @staticmethod
    def validate_common_name(value):
        if re.fullmatch(r"^[a-zA-Z\-\s']+$", value) is None:
            raise serializers.ValidationError(
                "Invalid entry for the plant's common name.")
        return value

    @staticmethod
    def validate_family_common_name(value):
        if re.fullmatch(r"^[a-zA-Z\-\s']+$", value) is None:
            raise serializers.ValidationError(
                "Invalid entry for the plant's family common name.")
        return value

    @staticmethod
    def validate_trefle_id(value):
        if not isinstance(value, int):
            raise serializers.ValidationError(
                "Invalid entry for the plant's Trefle ID.")
        return value
