from django.test import TestCase
from rest_framework import serializers

from backend.src.models.profile import Profile
from backend.src.serializers.profile_serializer import ProfileSerializer


class TestProfileSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestProfileSerializerValidators, cls).setUpClass()
        cls.test_obj = ProfileSerializer()


class TestSerializerParameters(TestProfileSerializerValidators):
    def test_serializer_parameters(self):
        self.assertEqual(
            ["profile_id", "first_name", "last_name", "gardens", "email_address"], self.test_obj.Meta.fields)
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
            "Your first name can only contain letters and must be 3 or more characters long.",
            self.test_obj.validate_first_name,
            first_name
        )

    def test_first_name_too_short(self):
        first_name = "Ry"

        self.assertRaisesMessage(
            serializers.ValidationError,
            "Your first name can only contain letters and must be 3 or more characters long.",
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
            "Your last name can only contain letters and must be 3 or more characters long.",
            self.test_obj.validate_last_name,
            last_name
        )

    def test_last_name_too_short(self):
        last_name = "Ry"

        self.assertRaisesMessage(
            serializers.ValidationError,
            "Your last name can only contain letters and must be 3 or more characters long.",
            self.test_obj.validate_last_name,
            last_name
        )


class TestValidateEmailAddress(TestProfileSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateEmailAddress, cls).setUpClass()

    def test_valid_email_address(self):
        email_address = "foo@bar.com"
        self.assertEqual(email_address, self.test_obj.validate_email_address(email_address))

    def test_invalid_email_address(self):
        invalid_email_address = "Foo_123.com"

        self.assertRaisesMessage(
            serializers.ValidationError,
            "Your email address is invalid.",
            self.test_obj.validate_email_address,
            invalid_email_address
        )
