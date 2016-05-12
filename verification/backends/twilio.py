# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Third party
from twilio.rest.client import TwilioRestClient

# Local
from .base import BaseBackend


class TwilioBackend(BaseBackend):
    default_message = "Welcome, click on the link to continue: {link}"

    def __init__(self, **options):
        super(TwilioBackend, self).__init__(**options)
        # Lower case it just to be sure
        options = {key.lower(): value for key, value in options.items()}

        if not options:
            raise ValueError('Missing sid, secret, from, for TwilioBackend')

        self._sid = options.get('sid')
        self._secret = options.get('secret')
        self._from = options.get('from')
        self._message = options.get('message', self.default_message)

        self.client = TwilioRestClient(account=self._sid, token=self._secret)

    def send(self, number, url):
        message = self._generate_message(url)
        return self.client.messages.create(to=number, body=message, from_=self._from)

    def _generate_message(self, url):
        return self._message.format(link=url)
