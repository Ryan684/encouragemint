import re

from rest_framework import serializers

from encouragemint.encouragemint.models import Profile, Plant


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["profile_id", "first_name", "last_name"]
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


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ["profile", "plant_name"]
        read_only_fields = ["profile"]

    @staticmethod
    def validate_plant_name(value):
        if re.fullmatch(r"^[a-zA-Z]+$", value) is None:
            raise serializers.ValidationError("A plant's name can only contain letters.")
        return value
