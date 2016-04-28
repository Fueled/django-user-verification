# -*- coding: utf-8 -*-

# Third party
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.conf import settings

# Smash stuff
from .serializers import PhoneVerificationSerializer


class VerificationViewSet(viewsets.GenericViewSet):

    @list_route(methods=['POST'], permission_classes=[AllowAny])
    def phone(self, request):
        serializer = PhoneVerificationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.send()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VerificationRedirectorView(TemplateView):
    def get_context_data(self, code=None, *args, **kwargs):
        context = super(VerificationRedirectorView, self).get_context_data(*args, **kwargs)
        context['redirect_url'] = "{}{}/{}".format(
            settings.PHONE_VERIFICATION.get('APP_URL'),
            settings.PHONE_VERIFICATION.get('APP_PATH', 'phone_verification'), code)

        return context
