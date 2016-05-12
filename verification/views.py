# -*- coding: utf-8 -*-

# Third party
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

# Local Stuff
from verification.serializers import VerificationSerializer
from verification.services import get_service


class VerificationRedirectorView(TemplateView):
    def get_context_data(self, code=None, *args, **kwargs):
        context = super(VerificationRedirectorView, self).get_context_data(*args, **kwargs)
        context['redirect_url'] = "{}{}/{}".format(
            settings.PHONE_VERIFICATION.get('APP_URL'),
            settings.PHONE_VERIFICATION.get('APP_PATH', 'phone_verification'), code)

        return context


class SendVerificationAPIView(generics.CreateAPIView):
    serializer_class = VerificationSerializer

    def post(self, request, verification_type=None):
        try:
            service = get_service(verification_type)
        except ValueError as e:
            raise Http404(e)

        recipient = self.request.data.get(verification_type, None)
        if not recipient:
            raise ValidationError("recipient is required.")

        service.send_verification(recipient, request)
        return Response(status=status.HTTP_204_NO_CONTENT)
