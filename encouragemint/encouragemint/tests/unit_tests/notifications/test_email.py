from django.core import mail
from django.test import TestCase

from encouragemint.encouragemint.models.garden import Garden
from encouragemint.encouragemint.notifications.email import send_garden_registered_email
from encouragemint.encouragemint.tests.helpers import create_test_garden


class EmailTestCase(TestCase):
    def setUp(self):
        garden_id = create_test_garden()["garden_id"]
        test_garden = Garden.objects.get(garden_id=garden_id)
        self.user_first_name = test_garden.profile.first_name
        self.user_garden_name = test_garden.garden_name
        self.user_email_address = test_garden.profile.email_address

    def _validate_email(self, expected_body, expected_subject):
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual("encouragemint.do.not.reply@gmail.com", mail.outbox[0].from_email)
        self.assertEqual([self.user_email_address], mail.outbox[0].to)
        self.assertEqual(expected_subject, mail.outbox[0].subject)
        self.assertEqual(expected_body, mail.outbox[0].body)


class TestSendGardenRegisteredEmail(EmailTestCase):
    def test_email_notification(self):
        expected_body = (
            f"Hey {self.user_first_name},\n\n"
            f"Your garden, {self.user_garden_name}, is now ready for plants.\n\n"
            "Thanks,\n"
            "Encouragemint"
        )
        expected_subject = f"{self.user_garden_name} is ready for plants"

        send_garden_registered_email(
            self.user_email_address, self.user_garden_name, self.user_first_name)

        self._validate_email(expected_body, expected_subject)

