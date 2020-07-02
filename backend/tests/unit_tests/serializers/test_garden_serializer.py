from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import serializers

from backend.src.models.garden import Garden
from backend.src.serializers.garden_serializer import GardenSerializer
from backend.tests.helpers import generate_new_user_payload


class TestGardenSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestGardenSerializerValidators, cls).setUpClass()
        cls.test_obj = GardenSerializer()


class TestSerializerParameters(TestGardenSerializerValidators):
    def test_serializer_parameters(self):
        self.assertEqual(
            ["garden_id", "garden_name", "plants", "user", "direction",
             "sunlight", "shade_tolerance", "location", "latitude", "longitude"],
            self.test_obj.Meta.fields)
        self.assertEqual(["garden_id", "user", "sunlight", "shade_tolerance"],
                         self.test_obj.Meta.read_only_fields)
        self.assertEqual(Garden, self.test_obj.Meta.model)


class TestValidateGardenName(TestGardenSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateGardenName, cls).setUpClass()

    def test_valid_garden_name(self):
        garden_name = "Backyard"
        self.assertEqual(garden_name, self.test_obj.validate_garden_name(garden_name))

    def test_invalid_garden_name(self):
        garden_name = "Backyard_123"

        self.assertRaisesMessage(
            serializers.ValidationError,
            f"Invalid entry for the garden's name. "
            f"A garden's name can only contain letters, numbers, hyphens, spaces and apostrophes.",
            self.test_obj.validate_garden_name,
            garden_name
        )


class TestValidateDirection(TestGardenSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateDirection, cls).setUpClass()

    def test_valid_direction(self):
        direction = "north"
        self.assertEqual(direction, self.test_obj.validate_direction(direction))

    def test_invalid_direction(self):
        direction = "down"

        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A garden's direction can only be north, east, south or west.",
            self.test_obj.validate_direction,
            direction
        )


class TestValidateSunlight(TestGardenSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateSunlight, cls).setUpClass()

    def test_direction_sunlight_scenarios(self):
        self._validate_sunlight_by_direction("north", "low")
        self._validate_sunlight_by_direction("south", "high")
        self._validate_sunlight_by_direction("east", "medium")
        self._validate_sunlight_by_direction("west", "medium")

    def _validate_sunlight_by_direction(self, direction, expected_sunlight):
        user = User.objects.create(**generate_new_user_payload())
        garden = Garden.objects.create(
            **{
                "garden_name": "Backyard",
                "user": user,
                "direction": direction,
                "location": "Truro, UK",
                "latitude": 50.263195,
                "longitude": -5.051041
            }
        )
        self.assertEqual(expected_sunlight, garden.sunlight)


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
