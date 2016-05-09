# -*- coding: utf-8 -*-

# Third party
from django.conf import settings
from django.utils.module_loading import import_string

DEFAULT_SERVICE = 'verification.backends.base.BaseBackend'

phone_backend = None
email_backend = None


def get_phone_backend():
    """
    Returns the general phone backend.

    :returns: base.BaseBackend inherited object.
    """
    global phone_backend

    if not phone_backend:
        phone_backend = get_backend(settings.PHONE_VERIFICATION)
    return phone_backend


def get_email_backend():
    """
    Returns the general email backend.
    :returns: base.BaseBackend inherited object.
    """
    global email_backend

    if not email_backend:
        email_backend = get_backend(settings.EMAIL_VERIFICATION)
    return email_backend


def get_backend(service_settings):
    """
    Gets the backend with the given service settings.
    It checks for a BACKEND key and later passes in these OPTIONS in the
    backend.

    :param service_settings: dict like object
    :returns: base.BaseBackend inherited object
    """
    backend_import = DEFAULT_SERVICE

    if service_settings.get('BACKEND', None):
        backend_import = service_settings['BACKEND']

    backend_cls = import_string(backend_import)
    return backend_cls(**service_settings['OPTIONS'])
