# Third Party Stuff
from django.test import TestCase
from nose.tools import ok_
from mock import patch

# Local Stuff
from verification.backends import get_phone_backend
from verification.backends.email import EmailBackend


class TwilioBackendTestCase(TestCase):

    def setUp(self):
        self.backend = get_phone_backend()

    @patch('twilio.rest.resources.messages.Messages.create')
    def test_send_message_two_numbers(self, mock):
        self.backend.send(numbers=['+15555555555', '+13333333333'], message='foo')
        ok_(mock.called)
        ok_(True)


class EmailBackendTestCase(TestCase):

    def setUp(self):
        self.backend = EmailBackend()
        self.emails = ['foo@bar.com', 'bar@foo.com']

    @patch('django.core.mail.send_mail')
    def test_send_message_two_emails(self, send_mail):
        self.backend.send(emails=self.emails, subject='bar', message='foo')
        ok_(send_mail.called)
