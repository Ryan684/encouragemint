from django.test import TestCase
from rest_framework import serializers

from encouragemint.encouragemint.serializers import GardenSerializer
from encouragemint.encouragemint.models import Garden


class TestGardenSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestGardenSerializerValidators, cls).setUpClass()
        cls.test_obj = GardenSerializer()


class TestSerializerParameters(TestGardenSerializerValidators):
    def test_serializer_parameters(self):
        self.assertEquals(["garden_id", "garden_name", "plants", "profile"], self.test_obj.Meta.fields)
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
            f"A garden's name can only contain letters.",
            self.test_obj.validate_garden_name,
            garden_name
        )
