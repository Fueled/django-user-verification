# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Third party
from twilio.rest.client import TwilioRestClient

# Local
from .base import BaseBackend


class TwilioBackend(BaseBackend):
    def __init__(self, **options):
        super(TwilioBackend, self).__init__(**options)
        # Lower case it just to be sure
        options = {key.lower(): value for key, value in options.items()}
        self._sid = options.get('sid', None)
        self._secret = options.get('secret', None)
        self._from = options.get('from', None)

        self.client = TwilioRestClient(account=self._sid, token=self._secret)

    def send_sms(self, number, message):
        self.client.messages.create(to=number, body=message, from_=self._from)

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(to=number, body=message, from_=self._from)
