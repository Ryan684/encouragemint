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


class TestValidateUsername(TestUserSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidateUsername, cls).setUpClass()

    def test_valid_username(self):
        username = "Ryan123"
        self.assertEqual(username, self.test_obj.validate_username(username))

    def test_invalid_username(self):
        self._assert_username_raises_error("Foo_123.bar")

    def test_username_too_short(self):
        self._assert_username_raises_error("Ry12")

    def _assert_username_raises_error(self, invalid_username):
        self.assertRaisesMessage(
            serializers.ValidationError,
            "Your username can only contain letters, numbers and must be 5 or more characters long.",
            self.test_obj.validate_username,
            invalid_username
        )


class TestValidatePassword(TestUserSerializerValidators):
    @classmethod
    def setUpClass(cls):
        super(TestValidatePassword, cls).setUpClass()

    def test_valid_password(self):
        password = "Ryan123!"
        self.assertEqual(password, self.test_obj.validate_password(password))

    def test_invalid_password_too_short(self):
        self._assert_password_raises_error("Foo!1")

    def test_invalid_password_no_numbers(self):
        self._assert_password_raises_error("Ry!ororor")

    def test_invalid_password_no_special_numbers(self):
        self._assert_password_raises_error("Ry1ororor")

    def test_invalid_password_no_letters(self):
        self._assert_password_raises_error("1234567!!")

    def _assert_password_raises_error(self, invalid_username):
        self.assertRaisesMessage(
            serializers.ValidationError,
            "Password must be at least 8 characters long, contain a digit and at least one special character.",
            self.test_obj.validate_password,
            invalid_username
        )