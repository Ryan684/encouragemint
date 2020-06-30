import re

from rest_framework import serializers

from backend.src.models.profile import Profile
from backend.src.serializers.garden_serializer import GardenSerializer


class ProfileSerializer(serializers.ModelSerializer):
    gardens = GardenSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ["profile_id", "first_name", "last_name", "gardens", "email_address"]
        read_only_fields = ["profile_id"]

    @staticmethod
    def validate_first_name(value):
        if re.fullmatch(r"^[a-zA-Z]{3,}$", value) is None:
            raise serializers.ValidationError(
                "Your first name can only contain letters and must be 3 or more characters long.",)
        return value

    @staticmethod
    def validate_last_name(value):
        if re.fullmatch(r"^[a-zA-Z]{3,}$", value) is None:
            raise serializers.ValidationError(
                "Your last name can only contain letters and must be 3 or more characters long.",)
        return value

    @staticmethod
    def validate_email_address(value):
        if re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", value) is None:
            raise serializers.ValidationError(
                "Your email address is invalid.")
        return value
