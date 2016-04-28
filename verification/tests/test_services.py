# -*- coding: utf-8 -*-

# Third Party Stuff
from django.test import TestCase
from nose.tools import ok_
from rest_framework.test import APIRequestFactory
from mock import patch

from verification.services import PhoneVerificationService


class PhoneVerifcationServiceTestCase(TestCase):
    def setUp(self):
        super(PhoneVerifcationServiceTestCase, self).setUp()
        self.service = PhoneVerificationService()

        factory = APIRequestFactory()
        self.request = factory.get('/')

        self.phone_number = '+13478379634'

    @patch('verification.backends.twilio.TwilioBackend.send_sms')
    def test_send_verification_generates_message_and_sends_message(self, mock):
        self.service.send_verification(self.phone_number, self.request)

        ok_(mock.called)

        args, kwargs = mock.call_args

        # Check if url is in
        ok_('verify' in args[1])
