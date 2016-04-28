# -*- coding: utf-8 -*-
from __future__ import absolute_import
import random

# Third party
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _


# Local
from .backends import get_phone_backend, get_email_backend

DEFAULT_EXPIRY = 3600 * 3
DEFAULT_MESSAGE = _("Welcome to {app}, continue with this link {link}")
SERVICES = {
    'phone_service': None,
    'email_service': None
}


class VerificationService(object):
    verification_message = settings.EMAIL_VERIFICATION.get('MESSAGE', DEFAULT_MESSAGE)

    def __init__(self, backend):
        self.backend = backend

    def send_verification(self, number, request):
        """
        Send a verification email to the given email to verify.

        :param number: the phone number of recipient.
        :param request: request it needs to point to (url)
        """
        if not number:
            raise ValueError('number required')

        key = self.create_temporary_token(number)
        url = self.create_url(request, key)
        message = self._generate_message(url)

        self.backend.send(number, message)

    def create_url(self, request, key):
        """
        Creates an URL for the redirect to the phone verification redirect
        page.

        :param request: request object, where the url needs to go to.
        :param key: The key to be added as a parameter.
        """
        if not key:
            raise ValueError('Key required')

        return request.build_absolute_uri(
            reverse('verification-redirector', kwargs={'code': key}))

    def create_temporary_token(self, number, expiry=DEFAULT_EXPIRY):
        """
        Creates a temporary token inside the cache, this holds the phone number
        as value, so that we can later check if everything is correct.

        :param number: Number of recipient
        :param expiry: Expiry of the token, defaults to 3 hours.

        :return token: string of sha token
        """
        token = cache.get(self._cache_key(number), self.generator())
        cache.set(self._cache_key(number), token, expiry)

        return token

    def _cache_key(self, number):
        return 'verification:{}'.format(number)

    def check_pin(self, token, phone_number):
        cached = cache.get(self._cache_key(phone_number))
        return str(token) == str(cached)

    @classmethod
    def generator(cls):
        """
        Returns an unique pin
        """
        return str(random.randint(10000, 99999))

    def _generate_message(self, url):
        return self.verification_message.format(app="Smash", link=url)


def get_email_service():
    email_service = VerificationService(backend=get_email_backend())
    SERVICES['email_service'] = email_service
    return email_service


def get_phone_service():
    phone_service = VerificationService(backend=get_phone_backend())
    SERVICES['phone_service'] = phone_service
    return phone_service
