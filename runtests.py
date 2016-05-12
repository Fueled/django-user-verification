import sys
import os

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="verification.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "verification",
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
        # PHONE VERIFICATION
        USER_VERIFICATION={
            'phone': {
                'BACKEND': 'verification.backends.twilio.TwilioBackend',
                'OPTIONS': {
                    'SID': os.getenv('TWILIO_API_SID', default='fake'),
                    'SECRET': os.getenv('TWILIO_API_SECRET', default='fake'),
                    'FROM': os.getenv('TWILIO_FROM', default='+14755292729'),
                    'MESSAGE': "Welcome, continue with this link: {link}"
                },
                'APP_URL': 'app://'
            },
            'email': {
                'BACKEND': 'verification.backends.email.EmailBackend',
                'OPTIONS': {
                    'FROM': os.getenv('FROM_EMAIL', default='dummy@fueled.com')
                },
                'APP_URL': 'app://'
            },

        },
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    #  Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
