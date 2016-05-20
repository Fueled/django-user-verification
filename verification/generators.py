# -*- coding: utf-8 -*-
import random

# Third party
from django.conf import settings
from django.utils.module_loading import import_string

DEFAULT_GENERATOR = 'verification.generators.NumberGenerator'


def get_generator(service_name):
    """
    Get the generator that is set for the specific service.
    """
    # Check if service_name in USER_VERIFICATION
    if not settings.USER_VERIFICATION.get(service_name, None):
        raise ValueError("{} not a valid service.".format(service_name))

    service_settings = settings.USER_VERIFICATION.get(service_name)
    generator_path = service_settings.get('GENERATOR', DEFAULT_GENERATOR)

    return import_string(generator_path)()


class Generator(object):
    pass


class NumberGenerator(Generator):
    """
    Creates a random number.

    :usage example:
        generator = NumberGenerator()
        print(generator())  # 123923
    """
    def __call__(self, key):
        return str(random.randint(10000, 99999))
