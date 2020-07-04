import re

from django.contrib.auth.models import User
from rest_framework import serializers

from backend.src.serializers.garden_serializer import GardenSerializer


class UserSerializer(serializers.ModelSerializer):
    gardens = GardenSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email", "gardens"]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):  # pylint: disable=no-self-use
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.save()
        return user

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
    def validate_email(value):
        if re.fullmatch(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", value) is None:
            raise serializers.ValidationError(
                "Your email address is invalid.")
        return value

    @staticmethod
    def validate_username(value):
        if re.fullmatch(r"^[a-zA-Z0-9\-]{5,}$", value) is None:
            raise serializers.ValidationError(
                "Your username can only contain letters, "
                "numbers and must be 5 or more characters long.")
        return value

    @staticmethod
    def validate_password(value):
        if re.fullmatch(
                r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", value) is None:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long, "
                "contain a digit and at least one special character.")
        return value
