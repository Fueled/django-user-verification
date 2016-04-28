# !/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
test_django-user-verification
------------

Tests for `services` models module.
"""

# Third Party Stuff
from django.test import TestCase
from nose.tools import ok_, raises
from rest_framework.test import APIRequestFactory
from mock import patch

# Local Stuff
from verification.services import VerificationService


class TestVerification(TestCase):

    @patch('verification.backends.twilio.TwilioBackend')
    def setUp(self, mock):
        self.service = VerificationService(backend=mock)
        factory = APIRequestFactory()
        self.request = factory.get('/')
        self.mock = mock
        self.phone_number = '+13478379634'

    def test_send_verification_with_valid_number_and_request(self):
        """ Test that send_verification with a valid number and request,
            is successful
        """
        self.service.send_verification(number=self.phone_number, request=self.request)
        ok_(self.mock.send.called)

    @raises(ValueError)
    def test_send_verification_with_no_number(self):
        """ Test that send_verification with no number specified
            raises a ValueError
        """
        self.service.send_verification('', self.request)

    def test_create_url_with_valid_request_and_key(self):
        """ Test that create_url with a valid request and key,
            is successful
        """
        key = self.service.create_temporary_token(self.phone_number)
        ok_(key in self.service.create_url(self.request, key))

    @raises(ValueError)
    def test_create_url_with_no_key(self):
        """ Test that create_url with no key
            raises ValueError
        """
        self.service.create_url(self.request, None)

    def test_create_temporary_token_with_valid_number(self):
        """ Test that create_temporary_token with valid number
            is successful
        """
        ok_(self.service.create_temporary_token(self.phone_number))

    def tearDown(self):
        pass
