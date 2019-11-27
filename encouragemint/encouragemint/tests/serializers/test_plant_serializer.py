from django.test import TestCase
from rest_framework import serializers

from encouragemint.encouragemint.serializers import PlantSerializer


class TestPlantSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPlantSerializerValidators, cls).setUpClass()
        cls.test_obj = PlantSerializer()


class TestValidateScientificName(TestPlantSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateScientificName, cls).setUpClass()

    def test_valid_scientific_name(self):
        scientific_name = "Rose"
        self.assertEqual(scientific_name, self.test_obj.validate_scientific_name(scientific_name))

    def test_invalid_scientific_name(self):
        scientific_name = "Rose_123"
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
        duration = "TODO"
        self.assertEqual(duration, self.test_obj.validate_duration(duration))

    def test_invalid_duration(self):
        duration = "TODO_123"
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
        bloom_period = "TODO"
        self.assertEqual(bloom_period, self.test_obj.validate_bloom_period(bloom_period))

    def test_invalid_bloom_period(self):
        bloom_period = "TODO_123"
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
        growth_period = "TODO"
        self.assertEqual(growth_period, self.test_obj.validate_growth_period(growth_period))

    def test_invalid_growth_period(self):
        growth_period = "TODO_123"
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
        growth_rate = "TODO"
        self.assertEqual(growth_rate, self.test_obj.validate_growth_rate(growth_rate))

    def test_invalid_growth_rate(self):
        growth_rate = "TODO_123"
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
        shade_tolerance = "TODO"
        self.assertEqual(shade_tolerance, self.test_obj.validate_shade_tolerance(shade_tolerance))

    def test_invalid_shade_tolerance(self):
        shade_tolerance = "TODO_123"
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
        moisture_use = "TODO"
        self.assertEqual(moisture_use, self.test_obj.validate_moisture_use(moisture_use))

    def test_invalid_moisture_use(self):
        moisture_use = "TODO_123"
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

    def test_valid_family_name(self):
        family_name = "TODO"
        self.assertEqual(family_name, self.test_obj.validate_family_name(family_name))

    def test_invalid_family_name(self):
        family_name = "TODO_123"
        self.assertRaisesMessage(
            serializers.ValidationError,
            f"A plant's family name can only contain letters.",
            self.test_obj.validate_family_name,
            family_name
        )
