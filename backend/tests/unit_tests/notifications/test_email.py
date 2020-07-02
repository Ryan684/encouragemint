from django.core import mail
from django.test import TestCase

from backend.src.models.garden import Garden
from backend.src.notifications.email import send_garden_registered_email, send_user_created_email, \
    send_garden_location_not_found_email
from backend.tests.helpers import create_test_garden


class EmailTestCase(TestCase):
    def setUp(self):
        garden_id = create_test_garden()["garden_id"]
        test_garden = Garden.objects.get(garden_id=garden_id)
        self.user_first_name = test_garden.user.first_name
        self.user_email = test_garden.user.email
        self.user_garden_name = test_garden.garden_name
        self.user_garden_location = test_garden.location

    def _validate_email(self, expected_body, expected_subject):
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual("encouragemint.do.not.reply@gmail.com", mail.outbox[0].from_email)
        self.assertEqual([self.user_email], mail.outbox[0].to)
        self.assertEqual(expected_subject, mail.outbox[0].subject)
        self.assertEqual(expected_body, mail.outbox[0].body)


class TestSendUserCreatedEmail(EmailTestCase):
    def test_email_notification(self):
        expected_body = (
            f"Welcome to Encouragemint {self.user_first_name}!\n\n"
            "Get started by adding a garden to your profile.\n\n"
            "Thanks,\n"
            "Encouragemint"
        )
        expected_subject = f"Welcome to Encouragemint"

        send_user_created_email(self.user_email, self.user_first_name)

        self._validate_email(expected_body, expected_subject)


class TestSendGardenRegisteredEmail(EmailTestCase):
    def test_email_notification(self):
        expected_body = (
            f"Hey {self.user_first_name},\n\n"
            f"Your garden {self.user_garden_name} is now ready for plants.\n\n"
            "Thanks,\n"
            "Encouragemint"
        )
        expected_subject = f"{self.user_garden_name} is ready for plants"

        send_garden_registered_email(
            self.user_email, self.user_garden_name, self.user_first_name)

        self._validate_email(expected_body, expected_subject)


class TestSendGardenLocationNotFoundEmail(EmailTestCase):
    def test_email_notification(self):
        expected_body = (
            f"Hey {self.user_first_name},\n\n"
            f"The location for your new garden {self.user_garden_location} couldn't be found.\n\n"
            "Please double check the address you gave us and try again.\n\n"
            "Thanks,\n"
            "Encouragemint"
        )
        expected_subject = f"{self.user_garden_name} couldn't be created"

        send_garden_location_not_found_email(
            self.user_email, self.user_garden_name, self.user_first_name, self.user_garden_location)

        self._validate_email(expected_body, expected_subject)

