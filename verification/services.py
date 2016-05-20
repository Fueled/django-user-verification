# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Third party
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings

# Local
from .backends import get_backend
from .generators import get_generator

DEFAULT_EXPIRY = 3600 * 3
services = {}


class VerificationService(object):
    """
    The VerificationService is the main access point in this module. This
    service makes sure that there is a token generated as well as it has been
    send with the appropriate backend.

    :ivar backend: the backend to be used (e.g. email, phone backend)
    :ivar verification_type: The type of verification that is done (e.g. email, phone)
    :ivar generator: Generator which returns a token to be passed
    """
    def __init__(self, backend, verification_type):
        super(VerificationService, self).__init__()

        self.backend = backend
        self.verification_type = verification_type
        self.generator = get_generator(verification_type)

    def send_verification(self, recipient, request):
        """
        Send a verification email/ text to the given recipient to verify.

        :param recipient: the phone recipient/ email of recipient.
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

    def create_temporary_token(self, recipient, expiry=DEFAULT_EXPIRY):
        """
        Creates a temporary token inside the cache, this holds the phone recipient
        as value, so that we can later check if everything is correct.

        :param recipient: recipient of recipient
        :param expiry: Expiry of the token, defaults to 3 hours.

        :return token: string of sha token
        """
        token = cache.get(self._cache_key(recipient), self.generator(recipient))
        cache.set(self._cache_key(recipient), token, expiry)

        return token

    def _cache_key(self, recipient):
        return 'verification:{}'.format(recipient)

    def validate_token(self, token, value):
        """
        Check if given token is valid, compares it with the ones present in the
        cache.

        :param token: Token to be checked
        :param value: The key it should be in

        :returns boolean: Valid or not.
        """
        cached = cache.get(self._cache_key(value))
        return str(token) == str(cached)


def get_service(service_name):
    """
    Gets the service VerificationService, checks if there is already one in the
    memory, if so return that one.

    :param service_name: e.g. phone, email
    """
    # Check if service_name in USER_VERIFICATIOn
    if not settings.USER_VERIFICATION.get(service_name, None):
        raise ValueError("{} not a valid service.".format(service_name))

    if not services.get(service_name, None):
        service = VerificationService(get_backend(service_name), service_name)
        services[service_name] = service
    return services[service_name]
