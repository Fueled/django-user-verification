# -*- coding: utf-8 -*-

# Third party


class BaseBackend(object):
    def __init__(self, **settings):
        pass

    def send(self, recipient, message):
        pass
