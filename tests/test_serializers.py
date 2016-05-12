# !/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
test_django-user-verification
------------

Tests for verification `serializers`.
"""

# Third Party Stuff
from django.test import TestCase
from rest_framework import serializers
from nose.tools import ok_, raises
from rest_framework.serializers import ValidationError
from mock import patch, MagicMock

# Local Stuff
from verification.serializers import VerificationSerializer
from verification.services import VerificationService


class TestVerification(TestCase):

    class TestSerializer(VerificationSerializer):
        email = serializers.CharField()
        token = serializers.CharField()

        class Meta:
            verification_type = 'email'
            token_field = 'token'

    def setUp(self):
        self.serializer = self.TestSerializer
        self.service_name = 'email'
        self.mock_data = {
            self.service_name: 'test@msn.com',
            'token': '1234'
        }

    @raises(ValidationError)
    def test_validate_with_no_token(self):
        data = self.mock_data
        data['token'] = ''

        serializer = self.serializer(data=data)
        serializer.is_valid(raise_exception=True)

    @raises(ValidationError)
    def test_validate_with_no_value(self):
        data = self.mock_data
        data[self.service_name] = ''

        serializer = self.serializer(data=data)
        serializer.is_valid(raise_exception=True)

    @patch.object(VerificationService, 'validate_token', return_value=True)
    def test_validate_with_valid_token_and_value(self, mock):
        serializer = self.serializer(data=self.mock_data)
        serializer.is_valid(raise_exception=True)

        ok_(mock.called)
