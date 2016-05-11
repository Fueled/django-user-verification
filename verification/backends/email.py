# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Third party
from django.template import Context
from django.template import loader
from django.core.mail import EmailMultiAlternatives

# Local
from .base import BaseBackend


class EmailBackend(BaseBackend):
    html_template = 'verification/email.html'
    subject = 'Please verify your email'

    def __init__(self, **options):
        super(EmailBackend, self).__init__(**options)
        # Lower case it just to be sure
        options = {key.lower(): value for key, value in options.items()}
        self.from_email = options.get('from_email', None)
        self.html_template = options.get('html_template', self.html_template)
        self.subject = options.get('subject', self.subject)

    def send(self, email, link):
        html = self._create_html(link)
        msg = EmailMultiAlternatives(self.subject, None, self.from_email,
                                     [email])
        msg.attach_alternative(html, "text/html")
        return msg.send()

    def _create_html(self, link):
        html_content = loader.get_template(self.html_template)

        context = Context({
            'url': link
        })
        return html_content.render(context)
