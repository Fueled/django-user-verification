# !/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
test_django-user-verification
------------

Tests for verification `generators`.
"""

# Third Party Stuff
from django.test import TestCase
from nose.tools import ok_

# Local Stuff
from verification.generators import NumberGenerator


class TestNumberGenerator(TestCase):
    def setUp(self):
        self.generator = NumberGenerator()

    def test_return_number_generator_returns_number(self):
        number = self.generator("test")
        ok_(number.isdigit())
