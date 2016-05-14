# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Third party
from django.template import Context
from django.template import loader
from django.core.mail import EmailMultiAlternatives

# Local
from .base import BaseBackend


class EmailBackend(BaseBackend):
    plaintext_template = 'verification/email.txt'
    html_template = 'verification/email.html'
    subject = 'Please verify your email'

    def __init__(self, **options):
        super(EmailBackend, self).__init__(**options)

        # Lower case it just to be sure
        options = {key.lower(): value for key, value in options.items()}
        self.from_email = options.get('from_email', None)
        self.html_template = options.get('html_template', self.html_template)
        self.plaintext_template = options.get('plaintext_template', self.plaintext_template)
        self.subject = options.get('subject', self.subject)

    def send(self, email, link):
        html = self._create_template(self.html_template, link)
        text = self._create_template(self.plaintext_template, link)
        msg = EmailMultiAlternatives(self.subject, text, self.from_email,
                                     [email])
        msg.attach_alternative(html, "text/html")
        return msg.send()

    @classmethod
    def _create_template(cls, template_name, link):
        html_content = loader.get_template(template_name)

        context = Context({
            'link': link
        })
        return html_content.render(context)
