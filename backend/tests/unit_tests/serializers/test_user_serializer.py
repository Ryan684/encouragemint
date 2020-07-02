from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import serializers

from backend.src.serializers.user_serializer import UserSerializer


class TestUserSerializerValidators(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestUserSerializerValidators, cls).setUpClass()
        cls.test_obj = UserSerializer()


class TestSerializerParameters(TestUserSerializerValidators):
    def test_serializer_parameters(self):
        self.assertEqual(
            ["username", "password", "first_name", "last_name", "email", "gardens"],
            self.test_obj.Meta.fields
        )
        self.assertEqual(["id"], self.test_obj.Meta.read_only_fields)
        self.assertEqual(User, self.test_obj.Meta.model)


class TestValidateFirstName(TestUserSerializerValidators):
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


class TestValidateLastName(TestUserSerializerValidators):
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


class TestValidateEmail(TestUserSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateEmail, cls).setUpClass()

    def test_valid_email(self):
        email_address = "foo@bar.com"
        self.assertEqual(email_address, self.test_obj.validate_email(email_address))

    def test_invalid_email(self):
        invalid_email_address = "Foo_123.com"

        self.assertRaisesMessage(
            serializers.ValidationError,
            "Your email address is invalid.",
            self.test_obj.validate_email,
            invalid_email_address
        )
