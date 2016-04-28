# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

# Third party stuff
from django.core.urlresolvers import reverse
from nose.tools import ok_
from mock import patch

# Local stuff
from base.tests import BaseTestCase


class VerificationViewSetTestCase(BaseTestCase):
    """
    Tests /verification endpoints
    """

    @patch('verification.services.PhoneVerificationService.send_verification')
    def test_valid_phone_number_triggers_sending_text_message(self, mock):
        url = reverse('verification-phone')
        data = {
            'phone_number': '+13478379634'
        }

        response = self.client.post(url, data)

        ok_(response.status_code, 204)
        ok_(mock.called)

    @patch('verification.services.PhoneVerificationService.send_verification')
    def test_invalid_phone_number_does_not_send_text_message(self, mock):
        url = reverse('verification-phone')
        data = {
            'phone_number': '+13214165'
        }

        response = self.client.post(url, data)

        ok_(response.status_code, 400)
        ok_(not mock.called)
