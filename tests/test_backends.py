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
import mock

# Local Stuff
from verification.backends.twilio import TwilioBackend
from twilio.rest.resources import Messages

class TestTwilioBackend(TestCase):

    @mock.patch('twilio.rest.client.TwilioRestClient')
    @mock.patch('twilio.rest.client.resources.Messages')
    def setUp(self, mock_twilio_rest_client, mock_messages):
        mock_twilio_rest_client.messages = mock_messages
        self.backend = TwilioBackend(sid='some_sid', secret='some_secret', from_number='+15555555555')
    
    def test_send_blank_message(self, mock):
        self.backend.send(numbers=['+15555555555'], message='')

        ok_(mock.called)

    @mock.patch('twilio.rest.client.TwilioRestClient')
    def test_send_not_blank_message(self, mock):
        self.backend.send(numbers=['+15555555555'], message='foo')

        ok_(mock.called)

    @mock.patch('twilio.rest.client.TwilioRestClient')
    def test_send_with_no_numbers(self, mock):
        self.backend.send(numbers=[], message='foo')

        ok_(mock.called)
        self.assertRaises(ValueError)

    def tearDown(self):
        pass
