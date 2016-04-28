# -*- coding: utf-8 -*-

# Third party
from django.conf import settings
from django.utils.module_loading import import_string

DEFAULT_SERVICE = 'verification.backends.base.BaseBackend'

phone_backend = None
email_backend = None


def get_phone_backend():
    if not phone_backend:
        backend_import = DEFAULT_SERVICE

        if settings.PHONE_VERIFICATION.get('BACKEND', None):
            backend_import = settings.PHONE_VERIFICATION['BACKEND']

        backend_cls = import_string(backend_import)
        return backend_cls(**settings.PHONE_VERIFICATION['OPTIONS'])


def get_email_backend():
    if not email_backend:
        backend_import = DEFAULT_SERVICE

        if settings.EMAIL_VERIFICATION.get('BACKEND', None):
            backend_import = settings.EMAIL_VERIFICATION['BACKEND']

        backend_cls = import_string(backend_import)
        return backend_cls(**settings.EMAIL_VERIFICATION['OPTIONS'])