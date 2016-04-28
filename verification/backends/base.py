# -*- coding: utf-8 -*-

# Third party


class BaseBackend(object):
    def __init__(self, **settings):
        pass

    def send_sms(self, numbers, message):
        pass

    def send_bulk_sms(self, numbers, message):
        pass
