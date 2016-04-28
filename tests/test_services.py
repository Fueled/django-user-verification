# !/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
test_django-user-verification
------------

Tests for `services` models module.
"""

# Third Party Stuff
from django.test import TestCase
from nose.tools import ok_
from rest_framework.test import APIRequestFactory
from mock import patch
from time import sleep

# Local Stuff
from verification.services import PhoneVerificationService


class TestVerification(TestCase):

    def setUp(self):
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

    def test_create_url_generates_absolute_uri_for_verify_endpoint(self):
        uri = self.service.create_url(self.request, 'key')
        self.assertEquals(uri, 'http://testserver/verify/key/')

    @patch('verification.services.PhoneVerificationService.generator')
    def test_create_temporary_token_with_default_expiry(self, mock):
        mock.return_value = 55555
        token = self.service.create_temporary_token(number=self.phone_number)
        self.assertEquals(token, 55555)
        self.assertEquals(self.service.check_pin(token, self.phone_number), True)


    @patch('verification.services.PhoneVerificationService.generator')
    def test_create_temporary_token_with_expiry_value_zero(self, mock):
        mock.return_value = 55555
        token = self.service.create_temporary_token(number=self.phone_number, expiry=0)
        sleep(1)
        self.assertEquals(self.service.check_pin(token, self.phone_number), False)


    def tearDown(self):
        pass
