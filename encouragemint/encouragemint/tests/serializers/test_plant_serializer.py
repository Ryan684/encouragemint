from django.test import TestCase
from rest_framework import serializers

from encouragemint.encouragemint.serializers import PlantSerializer
from encouragemint.encouragemint.models import Plant


class TestPlantSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPlantSerializerValidators, cls).setUpClass()
        cls.test_obj = PlantSerializer()


class TestSerializerParameters(TestPlantSerializerValidators):
    def test_serializer_parameters(self):
        self.assertEquals(
            ["plant_id", "garden", "common_name", "trefle_id", "scientific_name", "duration", "bloom_period",
             "growth_period", "growth_rate", "shade_tolerance", "moisture_use", "family_common_name"],
            self.test_obj.Meta.fields
        )
        self.assertEquals(["plant_id", "garden"], self.test_obj.Meta.read_only_fields)
        self.assertEquals(Plant, self.test_obj.Meta.model)


class TestValidateScientificName(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateScientificName, cls).setUpClass()

    def test_valid_scientific_name(self):
        scientific_name = "Roseus. Von-Bush"
        self.assertEqual(scientific_name, self.test_obj.validate_scientific_name(scientific_name))

    def test_invalid_scientific_name(self):
        scientific_name = "Rose*123"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's scientific name can only contain letters.",
            self.test_obj.validate_scientific_name,
            scientific_name
        )


class TestValidateDuration(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateDuration, cls).setUpClass()

    def test_valid_duration(self):
        duration = "Perennial"
        self.assertEqual(duration, self.test_obj.validate_duration(duration))

    def test_invalid_duration(self):
        duration = "Perennial_123"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's duration can only contain letters.",
            self.test_obj.validate_duration,
            duration
        )


class TestValidateBloomPeriod(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateBloomPeriod, cls).setUpClass()

    def test_valid_bloom_period(self):
        bloom_period = "Mid summer, Late summer"
        self.assertEqual(bloom_period, self.test_obj.validate_bloom_period(bloom_period))

    def test_invalid_bloom_period(self):
        bloom_period = "Mid_summer"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's bloom period can only contain letters.",
            self.test_obj.validate_bloom_period,
            bloom_period
        )


class TestValidateGrowthPeriod(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateGrowthPeriod, cls).setUpClass()

    def test_valid_growth_period(self):
        growth_period = "Spring, Summer"
        self.assertEqual(growth_period, self.test_obj.validate_growth_period(growth_period))

    def test_invalid_growth_period(self):
        growth_period = "Spring_Summer"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's growth period can only contain letters.",
            self.test_obj.validate_growth_period,
            growth_period
        )


class TestValidateGrowthRate(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateGrowthRate, cls).setUpClass()

    def test_valid_growth_rate(self):
        growth_rate = "Slow"
        self.assertEqual(growth_rate, self.test_obj.validate_growth_rate(growth_rate))

    def test_invalid_growth_rate(self):
        growth_rate = "Slow_123"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's growth rate can only contain letters.",
            self.test_obj.validate_growth_rate,
            growth_rate
        )


class TestValidateShadeTolerance(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateShadeTolerance, cls).setUpClass()

    def test_valid_shade_tolerance(self):
        shade_tolerance = "Intolerant"
        self.assertEqual(shade_tolerance, self.test_obj.validate_shade_tolerance(shade_tolerance))

    def test_invalid_shade_tolerance(self):
        shade_tolerance = "Intolerant_123"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's shade tolerance can only contain letters.",
            self.test_obj.validate_shade_tolerance,
            shade_tolerance
        )


class TestValidateMoistureUse(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateMoistureUse, cls).setUpClass()

    def test_valid_moisture_use(self):
        moisture_use = "Medium"
        self.assertEqual(moisture_use, self.test_obj.validate_moisture_use(moisture_use))

    def test_invalid_moisture_use(self):
        moisture_use = "Medium_123"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's moisture use can only contain letters.",
            self.test_obj.validate_moisture_use,
            moisture_use
        )


class TestValidateFamilyName(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateFamilyName, cls).setUpClass()

    def test_valid_family_common_name(self):
        family_name = "Rose Bushes"
        self.assertEqual(family_name, self.test_obj.validate_family_common_name(family_name))

    def test_invalid_family_name(self):
        family_name = "Rose*Bushes"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's family common name can only contain letters.",
            self.test_obj.validate_family_common_name,
            family_name
        )


class TestValidateTrefleID(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateTrefleID, cls).setUpClass()

    def test_valid_trefle_id(self):
        trefle_id = 123
        self.assertEqual(trefle_id, self.test_obj.validate_trefle_id(trefle_id))

    def test_invalid_trefle_id(self):
        trefle_id = "123"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's Trefle ID can only contain numbers.",
            self.test_obj.validate_trefle_id,
            trefle_id
        )


class TestValidateCommonName(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateCommonName, cls).setUpClass()

    def test_valid_common_name(self):
        common_name = "Rose Bushe"
        self.assertEqual(common_name, self.test_obj.validate_common_name(common_name))

    def test_invalid_common_name(self):
        common_name = "Rose*Bush"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's common name can only contain letters.",
            self.test_obj.validate_common_name,
            common_name
        )
