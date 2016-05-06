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
        
        if not options:
            raise ValueError('Missing sid, secret, from, for TwilioBackend')

        self._sid = options.get('sid')
        self._secret = options.get('secret')
        self._from = options.get('from')

        self.client = TwilioRestClient(account=self._sid, token=self._secret)

    def send(self, numbers, message):
        for number in numbers:
            self.client.messages.create(to=number, body=message, from_=self._from)
