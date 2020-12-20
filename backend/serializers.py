import re

from rest_framework import serializers

ALLOWED_SEASONS = ["SPRING", "SUMMER", "AUTUMN", "WINTER"]
ALLOWED_PLANT_DURATIONS = ["PERENNIAL", "ANNUAL", "BIENNIAL"]
ALLOWED_GARDEN_DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]


class RecommendSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    location = serializers.CharField()
    direction = serializers.CharField()
    duration = serializers.CharField()
    season = serializers.CharField()
    bloom_period = serializers.CharField()

    @staticmethod
    def validate_location(value):
        if re.fullmatch(r"^[a-zA-Z0-9\-\s',]+,[a-zA-Z0-9\-\s',]+$", value) is None:
            raise serializers.ValidationError(
                "Invalid entry for the garden's location. A garden's location can only "
                "contain letters, numbers, hyphens, spaces, commas and apostrophes. "
                "To be a valid location, you also have to have at least one degree of accuracy. "
                "For example; 'London' would not be valid, but 'London, UK' would work.")
        return value

    @staticmethod
    def validate_direction(value):
        direction = value.upper()
        if direction not in ALLOWED_GARDEN_DIRECTIONS:
            raise serializers.ValidationError(
                "A garden's direction can only be north, east, south or west.")
        return direction

    @staticmethod
    def validate_duration(value):
        duration = value.upper()
        if duration not in ALLOWED_PLANT_DURATIONS:
            raise serializers.ValidationError(
                "A garden's duration can only be perennial, annual or biennial.")
        return duration

    @staticmethod
    def validate_season(value):
        season = value.upper()
        if season not in ALLOWED_SEASONS:
            raise serializers.ValidationError(
                "A garden's season can only be spring, summer, autumn or winter.")
        return season

    @staticmethod
    def validate_bloom_period(value):
        bloom_period = value.upper()
        if bloom_period not in ALLOWED_SEASONS:
            raise serializers.ValidationError(
                "A garden's bloom period can only be spring, summer, autumn or winter.")
        return bloom_period
