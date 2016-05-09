# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Third party
from django.core import mail

# Local
from .base import BaseBackend


class EmailBackend(BaseBackend):
    """
    Email backend to send email with the Django Core email handler.

    :ivar from_email: The email where it needs to be send from.
    """
    def __init__(self, **options):
        super(EmailBackend, self).__init__(**options)

        # Lower case it just to be sure
        options = {key.lower(): value for key, value in options.items()}

        self.from_email = options.get('from_email')

    def send(self, emails, subject, message, html_message=None):
        """
        Sends an email with to the given emails.

        :param emails: iterative object with correctly formatted email
                       addresses, e.g:
                       - Shreyas <shreyas@fueled.com>
                       - paul@glemma.nl

        :param subject: Subject to be attached to email
        :param message: The raw email message
        :param html_message: The HTML formatted email message (default None)

        :returns bool: True or False for sent.
        """
        delivered_messages = mail.send_mail(
            from_email=self.from_email,
            subject=subject,
            message=message,
            fail_silently=False,
            recipient_list=emails)
        return delivered_messages
