import re

from rest_framework import serializers

from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.models.profile import Profile
from encouragemint.encouragemint.serializers.plant_serializer import PlantSerializer


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
