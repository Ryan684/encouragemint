import re

from rest_framework import serializers

from encouragemint.encouragemint.models import Profile, Plant, Garden


class PlantSerializer(serializers.ModelSerializer):
    garden = serializers.SlugRelatedField(slug_field="garden_id", queryset=Garden.objects.all())

    class Meta:
        model = Plant
        fields = ["plant_id", "garden", "trefle_id", "scientific_name", "duration",
                  "bloom_period", "growth_period", "growth_rate", "shade_tolerance",
                  "moisture_use", "family_name"]
        read_only_fields = ["plant_id", "garden"]

    @staticmethod
    def validate_scientific_name(value):
        if re.fullmatch(r"^[a-zA-Z\-\s.]+$", value) is None:
            raise serializers.ValidationError("A plant's scientific name can only contain letters.")
        return value

    @staticmethod
    def validate_duration(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("A plant's duration can only contain letters.")
        return value

    @staticmethod
    def validate_bloom_period(value):
        if re.fullmatch(r"^[a-zA-Z\s,]+$", value) is None:
            raise serializers.ValidationError("A plant's bloom period can only contain letters.")
        return value

    @staticmethod
    def validate_growth_period(value):
        if re.fullmatch(r"^[a-zA-Z\s,]+$", value) is None:
            raise serializers.ValidationError("A plant's growth period can only contain letters.")
        return value

    @staticmethod
    def validate_growth_rate(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("A plant's growth rate can only contain letters.")
        return value

    @staticmethod
    def validate_shade_tolerance(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("A plant's shade tolerance can only contain letters.")
        return value

    @staticmethod
    def validate_moisture_use(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("A plant's moisture use can only contain letters.")
        return value

    @staticmethod
    def validate_family_name(value):
        if re.fullmatch(r"^[a-zA-Z\-\s]+$", value) is None:
            raise serializers.ValidationError("A plant's family name can only contain letters.")
        return value

    @staticmethod
    def validate_trefle_id(value):
        if not isinstance(value, int):
            raise serializers.ValidationError("A plant's Trefle ID can only contain numbers.")
        return value


class GardenSerializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(slug_field="profile_id", queryset=Profile.objects.all())
    plants = PlantSerializer(many=True, read_only=True)

    class Meta:
        model = Garden
        fields = ["garden_id", "garden_name", "plants", "profile"]
        read_only_fields = ["garden_id", "profile"]

    @staticmethod
    def validate_garden_name(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("A garden's name can only contain letters.")
        return value


class ProfileSerializer(serializers.ModelSerializer):
    gardens = GardenSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ["profile_id", "first_name", "last_name", "gardens"]
        read_only_fields = ["profile_id"]

    @staticmethod
    def validate_first_name(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("Your first name can only contain letters.")
        return value

    @staticmethod
    def validate_last_name(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("Your last name can only contain letters.")
        return value
