# !/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
test_django-user-verification
------------

Tests for verification `views`.
"""
import random

# Third Party Stuff
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIClient
from nose.tools import eq_, ok_

# Local Stuff


class TestCreateVerification(APITestCase):

    def setUp(self):
        self.verification_type = random.choice(['email', 'phone'])
        self.url = reverse('verification-send', kwargs={'verification_type': self.verification_type})
        self.client = APIClient()
        self.data = {self.verification_type: {
            "email": "joe@doe.com",
            "phone": "+13476478477"
        }.get(self.verification_type, None)}

    def test_send_verification_with_valid_recipient_and_type(self):
        response = self.client.post(self.url, data=self.data, format='json')
        eq_(response.status_code, 204)

    def test_send_verification_with_valid_recipient_and_invalid_type(self):
        self.verification_type = ''
        self.url = reverse('verification-send', kwargs={'verification_type': 'asopmdasomd'})
        response = self.client.post(self.url, data=self.data, format='json')
        eq_(response.status_code, 404)

    def test_send_verification_invalid_recipient_and_valid_type(self):
        self.data[self.verification_type] = {}
        response = self.client.post(self.url, data=self.data, format='json')
        eq_(response.status_code, 400)
