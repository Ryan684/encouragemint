from django.test import TestCase
from rest_framework import serializers

from encouragemint.encouragemint.serializers import GardenSerializer
from encouragemint.encouragemint.models import Garden, Profile


class TestGardenSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestGardenSerializerValidators, cls).setUpClass()
        cls.test_obj = GardenSerializer()


class TestSerializerParameters(TestGardenSerializerValidators):
    def test_serializer_parameters(self):
        self.assertEquals(
            ["garden_id", "garden_name", "plants", "profile", "direction", "sunlight"], self.test_obj.Meta.fields)
        self.assertEquals(["garden_id", "profile"], self.test_obj.Meta.read_only_fields)
        self.assertEquals(Garden, self.test_obj.Meta.model)


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
        profile = Profile.objects.create(**{"first_name": "Jane", "last_name": "Doe"})
        garden = Garden.objects.create(
            **{"garden_name": "Backyard", "profile": profile, "direction": direction})
        self.assertEqual(expected_sunlight, garden.sunlight)
