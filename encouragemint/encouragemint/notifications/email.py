import logging

from django.core.mail import send_mail
from django.template.loader import render_to_string

FROM_ADDRESS = "encouragemint.do.not.reply@gmail.com"

logger = logging.getLogger("django")


def send_garden_registered_email(recipient, garden_name, first_name):
    template = "garden_registered"
    subject = f"{garden_name} is ready for plants"
    content = {"garden_name": garden_name, "first_name": first_name}

    _send_user_notification(content, subject, template, recipient)


def _send_user_notification(content, subject, template, recipient):
    message_as_text = render_to_string(f"{template}.txt", content)
    message_as_html = render_to_string(f"{template}.html", content)

    send_mail(subject, message_as_text, FROM_ADDRESS, [recipient], html_message=message_as_html)