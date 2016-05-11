# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Third party
from django.core import mail

# Local
from .base import BaseBackend


class EmailBackend(BaseBackend):
    def __init__(self, **options):
        super(EmailBackend, self).__init__(**options)
        # Lower case it just to be sure
        options = {key.lower(): value for key, value in options.items()}
        self.from_email = options.get('from_email')

    def send(self, emails, subject, message, html_message=None):
        delivered_messages = mail.send_mail(
                                       from_email=self.from_email,
                                       subject=subject,
                                       message=message,
                                       fail_silently=False,
                                       recipient_list=emails)
        return delivered_messages
