from django.test import TestCase

from encouragemint.encouragemint.models.plant import Plant
from encouragemint.encouragemint.serializers.plant_serializer import PlantSerializer


class TestPlantSerializer(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPlantSerializer, cls).setUpClass()
        cls.test_obj = PlantSerializer()


class TestSerializerParameters(TestPlantSerializer):
    def test_serializer_parameters(self):
        self.assertEqual(
            ["plant_id", "garden", "common_name", "trefle_id", "scientific_name",
             "duration", "bloom_period", "growth_period", "growth_rate", "shade_tolerance",
             "moisture_use", "family_common_name"],
            self.test_obj.Meta.fields
        )
        self.assertEqual(["plant_id", "garden"], self.test_obj.Meta.read_only_fields)
        self.assertEqual(Plant, self.test_obj.Meta.model)
