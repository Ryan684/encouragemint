import re

from rest_framework import serializers

from backend import seasons

ALLOWED_SEASONS = [
    seasons.EARLY_SPRING,
    seasons.LATE_SPRING,
    seasons.ALL_SPRING,
    seasons.EARLY_SUMMER,
    seasons.LATE_SUMMER,
    seasons.ALL_SUMMER,
    seasons.EARLY_AUTUMN,
    seasons.LATE_AUTUMN,
    seasons.EARLY_WINTER,
    seasons.LATE_WINTER,
    seasons.ALL_WINTER
]
ALLOWED_PLANT_DURATIONS = ["PERENNIAL", "ANNUAL", "BIENNIAL"]
ALLOWED_GARDEN_DIRECTIONS = ["NORTH", "EAST", "SOUTH", "WEST"]


class RecommendSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    location = serializers.CharField()
    duration = serializers.CharField()
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
    def validate_duration(value):
        duration = value.upper()
        if duration not in ALLOWED_PLANT_DURATIONS:
            raise serializers.ValidationError(
                f"A garden's duration can only be one of these periods: {ALLOWED_PLANT_DURATIONS}")
        return duration

    @staticmethod
    def validate_bloom_period(value):
        bloom_period = value.upper()
        if bloom_period not in ALLOWED_SEASONS:
            raise serializers.ValidationError(
                f"A garden's bloom period can only be one of these periods: {ALLOWED_SEASONS}")
        return bloom_period
