import re

from rest_framework import serializers

from encouragemint.encouragemint.models import Profile, Plant, Garden


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
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


class GardenSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    profile_id = serializers.PrimaryKeyRelatedField(
        queryset=Profile.objects.all(), source='profile', write_only=True)

    class Meta:
        model = Garden
        fields = "__all__"
        read_only_fields = ["garden_id"]

    @staticmethod
    def validate_garden_name(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("A garden's name can only contain letters.")
        return value


class PlantSerializer(serializers.ModelSerializer):
    garden = GardenSerializer(read_only=True)
    garden_id = serializers.PrimaryKeyRelatedField(
        queryset=Garden.objects.all(), source='garden', write_only=True)

    class Meta:
        model = Plant
        fields = "__all__"
        read_only_fields = ["plant_id"]

    @staticmethod
    def validate_plant_name(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("A plant's name can only contain letters.")
        return value
