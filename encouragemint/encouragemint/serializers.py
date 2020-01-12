import re

from rest_framework import serializers

from encouragemint.encouragemint.models import Profile, Plant, Garden


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


class GardenSerializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(slug_field="profile_id", queryset=Profile.objects.all())
    plants = PlantSerializer(many=True, read_only=True)
    sunlight = serializers.ReadOnlyField()
    latitude = serializers.ReadOnlyField()
    longitude = serializers.ReadOnlyField()

    class Meta:
        model = Garden
        fields = ["garden_id", "garden_name", "plants", "profile", "direction",
                  "sunlight", "location", "latitude", "longitude"]
        read_only_fields = ["garden_id", "profile", "sunlight"]

    @staticmethod
    def validate_garden_name(value):
        if re.fullmatch(r"^[a-zA-Z0-9\-\s']+$", value) is None:
            raise serializers.ValidationError(
                "Invalid entry for the garden's name. A garden's name can only "
                "contain letters, numbers, hyphens, spaces and apostrophes.")
        return value

    @staticmethod
    def validate_direction(value):
        direction = value.lower()
        if direction not in ["north", "east", "south", "west"]:
            raise serializers.ValidationError(
                "A garden's direction can only be north, east, south or west.")
        return direction

    @staticmethod
    def validate_location(value):
        if re.fullmatch(r"^[a-zA-Z0-9\-\s',]+,[a-zA-Z0-9\-\s',]+$", value) is None:
            raise serializers.ValidationError(
                "Invalid entry for the garden's location. A garden's location can only "
                "contain letters, numbers, hyphens, spaces, commas and apostrophes. "
                "To be a valid location, you also have to have at least one degree of accuracy. "
                "For example; 'London' would not be valid, but 'London, UK' would work.")
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
            raise serializers.ValidationError(
                "Your first name can only contain letters.")
        return value

    @staticmethod
    def validate_last_name(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError(
                "Your last name can only contain letters.")
        return value
