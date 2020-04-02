from django.test import TestCase
from rest_framework import serializers

from encouragemint.encouragemint.models.profile import Profile
from encouragemint.encouragemint.serializers.profile_serializer import ProfileSerializer


class TestProfileSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestProfileSerializerValidators, cls).setUpClass()
        cls.test_obj = ProfileSerializer()


class TestSerializerParameters(TestProfileSerializerValidators):
    def test_serializer_parameters(self):
        self.assertEqual(
            ["profile_id", "first_name", "last_name", "gardens"], self.test_obj.Meta.fields)
        self.assertEqual(["profile_id"], self.test_obj.Meta.read_only_fields)
        self.assertEqual(Profile, self.test_obj.Meta.model)


class TestValidateFirstName(TestProfileSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateFirstName, cls).setUpClass()

    def test_valid_first_name(self):
        first_name = "Ryan"
        self.assertEqual(first_name, self.test_obj.validate_first_name(first_name))

    def test_invalid_first_name(self):
        first_name = "Ryan_123"

        self.assertRaisesMessage(
            serializers.ValidationError,
            f"Your first name can only contain letters.",
            self.test_obj.validate_first_name,
            first_name
        )


class TestValidateLastName(TestProfileSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateLastName, cls).setUpClass()

    def test_valid_last_name(self):
        last_name = "Ryan"
        self.assertEqual(last_name, self.test_obj.validate_last_name(last_name))

    def test_invalid_last_name(self):
        last_name = "Ryan_123"

        self.assertRaisesMessage(
            serializers.ValidationError,
            f"Your last name can only contain letters.",
            self.test_obj.validate_last_name,
            last_name
        )
