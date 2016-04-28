========
Usage
========

Defining Environment Variables for Backend
-----------------

In your settings file (e.g. common.py), define your credentials and any environment variables required for your backend service (e.g. Sendgrid, Twilio). This is how django-user-verification will actually send its verification link to whichever clients.

Also, add "verification" in your **INSTALLED_APPS** that's in your settings file.

For example, we define backend env variables in our settings file for Twilio:   

.. code-block:: python

    # PHONE VERIFICATION
    PHONE_VERIFICATION = {
        'BACKEND': 'verification.backends.twilio.TwilioBackend',
        'OPTIONS': {
            'SID': env('TWILIO_API_SID', default='fake'),
            'SECRET': env('TWILIO_API_SECRET', default='fake'),
            'FROM': env('TWILIO_FROM', default='+14755292729')
        },
        'APP_URL': 'app://'
    }



To use verification in a project:
----------------------------

.. code-block:: python

    import verification

    # Send a verification to a phone
    from verification.services import PhoneVerificationService

    # Create a PhoneVerificationService instance
    service = PhoneVerificationService()

    # Send verification message to number
    service.send_verification(number='+15555555555')