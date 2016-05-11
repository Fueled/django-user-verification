# -*- coding: utf-8 -*-
from __future__ import absolute_import
import random

# Third party
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings

# Local
from .backends import get_backend

DEFAULT_EXPIRY = 3600 * 3
services = {}


class VerificationService(object):

    def __init__(self, backend, verification_type):
        self.backend = backend
        self.verification_type = verification_type

    def send_verification(self, recipient, request):
        """
        Send a verification email/ text to the given recipient to verify.

        :param recipient: the phone number/ email of recipient.
        :param request: request it needs to point to (url)
        """
        if not recipient:
            raise ValueError('recipient value is required.')

        key = self.create_temporary_token(recipient)
        url = self.create_url(request, key)

        return self.backend.send(recipient, url)

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
            reverse('verification-redirector', kwargs={'code': key,
                                                       'verification_type': self.verification_type}))

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

    def validate_token(self, token, value):
        cached = cache.get(self._cache_key(value))
        return str(token) == str(cached)

    @classmethod
    def generator(cls):
        """
        Returns an unique pin
        """
        return str(random.randint(10000, 99999))


def get_service(service_name):
    # Check if service_name in USER_VERIFICATIOn
    if not settings.USER_VERIFICATION.get(service_name, None):
        raise ValueError("{} not a valid service.".format(service_name))

    if not services.get(service_name, None):
        service = VerificationService(get_backend(service_name), service_name)
        services[service_name] = service
    return services[service_name]
