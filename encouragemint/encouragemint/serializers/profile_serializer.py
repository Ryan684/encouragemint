import re

from rest_framework import serializers

from encouragemint.encouragemint.models.profile import Profile
from encouragemint.encouragemint.serializers.garden_serializer import GardenSerializer


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
