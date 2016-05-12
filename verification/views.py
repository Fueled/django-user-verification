# -*- coding: utf-8 -*-

# Third party
from django.views.generic import TemplateView
from django.conf import settings

# Verification Stuff


class VerificationRedirectorView(TemplateView):
    def get_context_data(self, code=None, *args, **kwargs):
        context = super(VerificationRedirectorView, self).get_context_data(*args, **kwargs)
        context['redirect_url'] = "{}{}/{}".format(
            settings.PHONE_VERIFICATION.get('APP_URL'),
            settings.PHONE_VERIFICATION.get('APP_PATH', 'phone_verification'), code)

        return context