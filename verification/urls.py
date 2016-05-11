# -*- coding: utf-8 -*-

# Third Party Stuff
from rest_framework import routers
from django.conf.urls import url

# smash Stuff
from .views import VerificationRedirectorView, SendVerificationAPIView


urlpatterns = [
    url(r'^verify/send/(?P<verification_type>[0-9A-Za-z_\-]+)/$',
        SendVerificationAPIView.as_view(),
        name='verification-send'),
    url(r'^verify/(?P<verification_type>[0-9A-Za-z_\-]+)/(?P<code>[^/.]+)/$',
        VerificationRedirectorView.as_view(template_name="verification/redirector.html"),
        name='verification-redirector'),
]

router = routers.DefaultRouter(trailing_slash=False)
urlpatterns += router.urls
