========
Usage
========

Defining Environment Variables for Backend
-----------------

In your settings file (e.g. common.py), define your credentials and any environment variables required for your backend service (e.g. Sendgrid, Twilio). This is how django-user-verification will actually send its verification link to whichever clients.

Also, add "verification" in your **INSTALLED_APPS** that's in your settings file.

For example, we define backend env variables in our settings file for Twilio:

.. code-block:: python

        USER_VERIFICATION = {
            'phone': {
                'BACKEND': 'verification.backends.base.BaseBackend',
                'OPTIONS': {
                    'SID': os.getenv('TWILIO_API_SID', default='fake'),
                    'SECRET': os.getenv('TWILIO_API_SECRET', default='fake'),
                    'FROM': os.getenv('TWILIO_FROM', default='+14755292729'),
                    'MESSAGE': "Welcome, continue with this link: {link}"
                },
                'APP_URL': 'app://'
            },
            'email': {
                'BACKEND': 'verification.backends.base.BaseBackend',
                'OPTIONS': {
                    'FROM': os.getenv('FROM_EMAIL', default='dummy@fueled.com')
                },
                'APP_URL': 'app://'
            },
        }


To use verification in a project:
----------------------------

.. code-block:: python

    import verification

    # Send a verification to a phone
    from verification.services import get_phone_backend

    # Create a VerificationService instance with the phone backend
    service = get_phone_backend()

    # Send verification message to number
    service.send_verification(number='+15555555555')



Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py
