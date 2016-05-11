# -*- coding: utf-8 -*-

# Third Party Stuff
from rest_framework import routers
from django.conf.urls import url

# smash Stuff
from .views import VerificationRedirectorView


urlpatterns = [
    url(r'^verify/(?P<code>[^/.]+)/$',
        VerificationRedirectorView.as_view(template_name="verification/redirector.html"),
        name='verification-redirector'),
]

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns += router.urls
