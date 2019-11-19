from django.test import TestCase
from rest_framework import serializers

from encouragemint.encouragemint.serializers import PlantSerializer


class TestPlantSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPlantSerializerValidators, cls).setUpClass()
        cls.test_obj = PlantSerializer()


class TestValidatePlantName(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidatePlantName, cls).setUpClass()

    def test_valid_plant_name(self):
        plant_name = "Rose"
        self.assertEqual(plant_name, self.test_obj.validate_plant_name(plant_name))

    def test_invalid_plant_name(self):
        plant_name = "Rose_123"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's name can only contain letters.",
            self.test_obj.validate_plant_name,
            plant_name
        )
