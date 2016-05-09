# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Third party
from twilio.rest.client import TwilioRestClient

# Local
from .base import BaseBackend


class TwilioBackend(BaseBackend):
    """
    Backend to send messages with Twilio.

    :ivar _sid: Retrieved from options
    :ivar _secret: Retrieved from options
    :ivar _from: Retrieved from options
    :ivar client: TwilioRestClient
    """
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
        """
        Sends the given messages to the given numbers

        :param numbers: array/iterator like with numbers formatted e.g:
                        - +13478379633
                        - +31627853318

        :param message: message contents
        """
        for number in numbers:
            self.client.messages.create(to=number, body=message, from_=self._from)
