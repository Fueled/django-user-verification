# -*- coding: utf-8 -*
import random

# Third Party Stuff
from django.test import TestCase
from nose.tools import ok_
from mock import patch

# Local Stuff
from verification.backends.email import EmailBackend
from verification.backends.twilio import TwilioBackend


class TwilioBackendTestCase(TestCase):

    def setUp(self):
        self.backend = TwilioBackend(sid='poop', secret='foop', from_number='joop')

    @patch('twilio.rest.resources.messages.Messages.create')
    def test_send_message_two_numbers(self, mock):
        self.backend.send('+13333333333', 'foo')
        ok_(mock.called)
        ok_(True)


class EmailBackendTestCase(TestCase):

    def setUp(self):
        self.backend = EmailBackend()
        self.email = random.choice(['foo@bar.com', 'bar@foo.com'])
        self.url = 'http://link123'

    @patch('django.core.mail.EmailMultiAlternatives.send')
    def test_send_message_two_emails(self, send_mail):
        self.backend.send(self.email, self.url)
        ok_(send_mail.called)
