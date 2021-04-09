from django.test import TestCase
from rest_framework import serializers

from backend import serializers as backend_serializers, seasons


class TestGardenSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestGardenSerializerValidators, cls).setUpClass()
        cls.test_obj = backend_serializers.RecommendSerializer()


class TestValidateLocation(TestGardenSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateLocation, cls).setUpClass()

    def test_valid_location(self):
        location = "Falmouth, UK"
        self.assertEqual(location, self.test_obj.validate_location(location))

    def test_invalid_location(self):
        location = "Falmouth"

        self.assertRaisesMessage(
            serializers.ValidationError,
            f"Invalid entry for the garden's location. A garden's location can only "
            f"contain letters, numbers, hyphens, spaces, commas and apostrophes. "
            f"To be a valid location, you also have to have at least one degree of accuracy. "
            f"For example; 'London' would not be valid, but 'London, UK' would work.",
            self.test_obj.validate_location,
            location
        )


class TestValidateDuration(TestGardenSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateDuration, cls).setUpClass()

    def test_valid_uppercase_duration(self):
        duration = "PERENNIAL"
        self.assertEqual(duration, self.test_obj.validate_duration(duration))

    def test_valid_lowercase_duration(self):
        duration = "perennial"
        self.assertEqual("PERENNIAL", self.test_obj.validate_duration(duration))

    def test_invalid_duration(self):
        duration = "summer"

        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A garden's duration can only be one of these periods: {backend_serializers.ALLOWED_PLANT_DURATIONS}",
            self.test_obj.validate_duration,
            duration
        )


class TestValidateBloomPeriod(TestGardenSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateBloomPeriod, cls).setUpClass()

    def test_valid_uppercase_bloom_period(self):
        bloom_period = seasons.EARLY_SPRING
        self.assertEqual(bloom_period, self.test_obj.validate_bloom_period(bloom_period))

    def test_valid_lowercase_bloom_period(self):
        bloom_period = seasons.EARLY_SPRING.lower()
        self.assertEqual(seasons.EARLY_SPRING, self.test_obj.validate_bloom_period(bloom_period))

    def test_invalid_bloom_period(self):
        bloom_period = "march"

        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A garden's bloom period can only be one of these values: {backend_serializers.ALLOWED_SEASONS}",
            self.test_obj.validate_bloom_period,
            bloom_period
        )
